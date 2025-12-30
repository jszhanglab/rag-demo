from uuid import UUID
from app.repositories.document_repository import DocumentRepository
from app.repositories.ocr_result_repository import OCRResultRepository
from app.repositories.chunk_repository import ChunkRepository
from app.db.session import session_scope
from app.constants.status import DocumentStatus
from app.services.ocr_service import run_ocr
from app.services.chunk_service import chunk_text
from app.constants.status import OCRStatus
from app.utils.config import settings

def process_document_pipeline(document_id: str, lang: str = "en") -> None:
    doc_id = UUID(document_id)
    """
    This pipeline separates short-lived database transactions
    from long-running operations (e.g. OCR, chunking, embedding).
    Heavy tasks must not hold a DB session.

    document rag pipeline: ocr -> chunk -> embedding
    """
    try:
        with session_scope() as db:
            doc_repo = DocumentRepository(db)
            ocr_repo = OCRResultRepository(db)

            document = doc_repo.get_by_id(doc_id)
            if not document:
                return

            file_path = document.file_path

            # OCR start
            doc_repo.mark_status(document_id,DocumentStatus.OCR_PROCESSING)
            ocr_repo.mark_processing(document_id)

        # OCR
        ocr_text = run_ocr(file_path, lang=lang)

        # Save OCR text
        with session_scope() as db:
            doc_repo = DocumentRepository(db)
            ocr_repo = OCRResultRepository(db)
            doc_repo.mark_status(document_id,DocumentStatus.OCR_DONE)
            ocr_repo.mark_completed(document_id=document_id, text=ocr_text)

        # Chunks
        chunks_list = chunk_text(ocr_text,lang)

        # Save chunks
        with session_scope() as db:
            chunk_records = [
                    {
                        "document_id": doc_id,
                        "chunk_index": idx,
                        "start_offset": item["start"],
                        "end_offset": item["end"],
                        "token_count": len(item["text"]),
                        "text": item["text"],
                        "embedding_id": None
                    }
                    for idx, item in enumerate(chunks_list)
                ]
            chunk_repo = ChunkRepository(db)
            chunk_repo.delete_by_document_id(doc_id)
            chunk_repo.bulk_insert(chunk_records)
            doc_repo = DocumentRepository(db)
            doc_repo.mark_status(document_id,DocumentStatus.CHUNK_DONE)

        # TODO embedding stage

    except Exception as e:
        with session_scope() as db:
            try:
                OCRResultRepository(db).mark_failed(document_id=document_id, error_message=str(e))
            except Exception:
                pass
        raise