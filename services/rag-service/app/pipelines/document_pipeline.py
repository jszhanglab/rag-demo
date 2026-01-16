#services\rag-service\app\pipelines\document_pipeline.py

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
from transformers import AutoTokenizer

def process_document_pipeline(document_id: str, lang: str = "en") -> None:
    doc_id = UUID(document_id)
    """
    This pipeline separates short-lived database transactions
    from long-running operations (e.g. OCR, chunking, embedding).
    Heavy tasks must not hold a DB session.

    document rag pipeline: ocr -> chunk -> embedding
    """

    tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

    try:
        with session_scope() as db:
            doc_repo = DocumentRepository(db)
            ocr_repo = OCRResultRepository(db)

            document = doc_repo.get_by_id(doc_id)
            if not document:
                return

            file_path = document.file_path

            # OCR start
            doc_repo.mark_status(doc_id,DocumentStatus.OCR_PROCESSING)
            ocr_repo.mark_processing(doc_id)
        # -------------------------
        # OCR
        # -------------------------
        ocr_text = run_ocr(file_path, lang=lang)

        # Save OCR text
        with session_scope() as db:
            doc_repo = DocumentRepository(db)
            ocr_repo = OCRResultRepository(db)
            doc_repo.mark_status(doc_id,DocumentStatus.OCR_DONE)
            ocr_repo.mark_completed(document_id=doc_id, text=ocr_text)

        # -------------------------
        # Chunks
        # -------------------------
        chunks_list = chunk_text(ocr_text,lang)

        # Save chunks
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
            doc_repo.mark_status(doc_id,DocumentStatus.CHUNK_DONE)

        # -------------------------
        # Embedding stage
        # -------------------------

        # Mark embedding processing (short DB Transaction)
        with session_scope() as db:
            doc_repo = DocumentRepository(db)
            doc_repo.mark_status(doc_id, DocumentStatus.EMBEDDING_PROCESSING)

        # 1) Read chunks back from DB to get chunk.id (short DB txn)
        with session_scope() as db:
            chunk_repo = ChunkRepository(db)
            chunks = chunk_repo.list_by_document_id(doc_id)  # must return rows/ORM with .id, .text, etc.

            # detach necessary fields from session
            chunk_payloads = [
                {
                    "id": str(c.id),
                    "chunk_index": int(c.chunk_index),
                    "start_offset": c.start_offset,
                    "end_offset": c.end_offset,
                    "text": c.text,
                }
                for c in chunks
            ]

        # 2) Compute embeddings (heavy, no DB session)
        embedding_svc = EmbeddingService(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            normalize=True,
            batch_size=32,
            device=None,
        )
        texts = [x["text"] for x in chunk_payloads]
        vectors = embedding_svc.embed_texts(texts)

        # 3) Build metadatas (pure python)
        metadatas = [
            ChunkVectorMeta(
                document_id=str(doc_id),
                chunk_id=x["id"],
                chunk_index=x["chunk_index"],
                source="ocr",
                start_offset=x["start_offset"],
                end_offset=x["end_offset"],
                page=None,
            )
            for x in chunk_payloads
        ]

        # 4) Upsert to Chroma (index layer)
        chroma_repo = ChromaVectorRepository(
            persist_dir="uploaded_files/chroma",  # TODO move to config/env
            collection_name="rag_chunks",
        )
        chroma_repo.upsert_chunks(
            chunk_ids=[x["id"] for x in chunk_payloads],  # ids == chunk_id
            embeddings=vectors,
            documents=texts,
            metadatas=metadatas,
        )

        # 5) Mark done (short DB txn)
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