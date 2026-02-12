from uuid import UUID
from app.repositories.document_repository import DocumentRepository
from app.repositories.ocr_result_repository import OCRResultRepository
from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding_service import EmbeddingService
from app.vectorstore.chroma_repo import ChromaVectorRepository
from app.vectorstore.schemas import ChunkVectorMeta
from app.db.session import session_scope
from app.constants.status import DocumentStatus
from app.services.ocr_service import run_ocr
from app.services.chunk_service import chunk_text
from app.utils.config import settings
from transformers import AutoTokenizer
import os
import json

def process_document_pipeline(document_id: str, lang: str = "en") -> None:
    doc_id = UUID(document_id)
    
    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
    VECTOR_DB_URL = settings.VECTOR_DB_URL
    LLM_MODEL_DEV = settings.LLM_MODEL_DEV

    try:
        with session_scope() as db:
            doc_repo = DocumentRepository(db)
            ocr_repo = OCRResultRepository(db)

            document = doc_repo.get_by_id(doc_id)
            if not document:
                return

            file_path = document.file_path

            doc_repo.mark_status(doc_id, DocumentStatus.OCR_PROCESSING)
            ocr_repo.mark_processing(doc_id)

        # -------------------------
        # OCR Stage
        # -------------------------
        ocr_result_data = run_ocr(file_path, lang=lang)

        # Convert list/dict to JSON string to avoid 'psycopg2.ProgrammingError: can't adapt type dict'
        ocr_text_to_save = json.dumps(ocr_result_data, ensure_ascii=False)

        with session_scope() as db:
            doc_repo = DocumentRepository(db)
            ocr_repo = OCRResultRepository(db)
            doc_repo.mark_status(doc_id, DocumentStatus.OCR_DONE)
            ocr_repo.mark_completed(document_id=doc_id, ocr_text=ocr_text_to_save)

        # -------------------------
        # Chunks Stage
        # -------------------------
        chunks_list = chunk_text(ocr_result_data, lang)

        with session_scope() as db:
            chunk_records = [
                {
                    "document_id": doc_id,
                    "chunk_index": idx,
                    "start_offset": item["start"],
                    "end_offset": item["end"],
                    "token_count": len(tokenizer.encode(item["text"], add_special_tokens=False)),
                    "text": item["text"],
                    "embedding_id": None
                }
                for idx, item in enumerate(chunks_list)
            ]
            chunk_repo = ChunkRepository(db)
            chunk_repo.delete_by_document_id(doc_id)
            chunk_repo.bulk_insert(chunk_records)
            
            doc_repo = DocumentRepository(db)
            doc_repo.mark_status(doc_id, DocumentStatus.CHUNK_DONE)

        # -------------------------
        # Embedding Stage
        # -------------------------
        with session_scope() as db:
            doc_repo = DocumentRepository(db)
            doc_repo.mark_status(doc_id, DocumentStatus.EMBEDDING_PROCESSING)

        with session_scope() as db:
            chunk_repo = ChunkRepository(db)
            chunks = chunk_repo.list_by_document_id(doc_id)

            # Mapping page numbers from chunk_text results to chunk payloads
            chunk_payloads = []
            for idx, c in enumerate(chunks):
                current_page = chunks_list[idx].get("page") if idx < len(chunks_list) else None
                chunk_payloads.append({
                    "id": str(c.id),
                    "chunk_index": int(c.chunk_index),
                    "start_offset": c.start_offset,
                    "end_offset": c.end_offset,
                    "text": c.text,
                    "page": current_page
                })

        embedding_svc = EmbeddingService(
            model_name=LLM_MODEL_DEV,
            normalize=True,
            batch_size=32,
            device=None,
        )
        texts = [x["text"] for x in chunk_payloads]
        vectors = embedding_svc.embed_texts(texts)

        # -------------------------
        # Vector DB Stage
        # -------------------------
        metadatas = [
            ChunkVectorMeta(
                document_id=str(doc_id),
                chunk_id=x["id"],
                chunk_index=x["chunk_index"],
                source="ocr",
                start_offset=x["start_offset"],
                end_offset=x["end_offset"],
                page=x["page"], 
            )
            for x in chunk_payloads
        ]

        chroma_repo = ChromaVectorRepository(
            persist_dir=VECTOR_DB_URL,
            collection_name="rag_chunks",
        )
        chroma_repo.upsert_chunks(
            chunk_ids=[x["id"] for x in chunk_payloads],
            embeddings=vectors,
            documents=texts,
            metadatas=metadatas,
        )

        with session_scope() as db:
            doc_repo = DocumentRepository(db)
            doc_repo.mark_status(doc_id, DocumentStatus.EMBEDDING_DONE)

    except Exception as e:
        with session_scope() as db:
            try:
                OCRResultRepository(db).mark_failed(document_id=doc_id, error_message=str(e))
            except Exception:
                pass
        raise