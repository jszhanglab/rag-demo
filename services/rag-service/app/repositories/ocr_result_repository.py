# app/repositories/ocr_result_repository.py

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models.ocr_result import OCRResult
from app.constants.status import OCRStatus


class OCRResultRepository:
    """
    OCRResult repository (document_id is unique / one-to-one with OCRResult).

    Naming philosophy:
    - Basic CRUD: create/get/update/delete (clear and consistent)
    - Business intent helpers: mark_pending/mark_completed/mark_failed
    - Upsert: upsert_* always returns OCRResult (never Optional)
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        document_id: UUID,
        status: str,
        ocr_text: str = "",
        table_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
    ) -> OCRResult:
        obj = OCRResult(
            document_id=document_id,
            status=status,
            ocr_text=ocr_text,
            table_data=table_data,
            error_message=error_message,
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def get_by_document_id(self, document_id: UUID) -> Optional[OCRResult]:
        return (
            self.db.query(OCRResult)
            .filter(OCRResult.document_id == document_id)
            .first()
        )

    def update_by_document_id(
        self,
        document_id: UUID,
        *,
        status: Optional[str] = None,
        ocr_text: Optional[str] = None,
        table_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
    ) -> Optional[OCRResult]:
        obj = self.get_by_document_id(document_id)
        if obj is None:
            return None

        if status is not None:
            obj.status = status
        if ocr_text is not None:
            obj.ocr_text = ocr_text
        if table_data is not None:
            obj.table_data = table_data
        if error_message is not None:
            obj.error_message = error_message

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_by_document_id(self, document_id: UUID) -> bool:
        obj = self.get_by_document_id(document_id)
        if obj is None:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def upsert_by_document_id(
        self,
        document_id: UUID,
        *,
        status: str,
        ocr_text: str = "",
        table_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
    ) -> OCRResult:
        """
        Always returns OCRResult.
        """
        existing = self.get_by_document_id(document_id)
        if existing is not None:
            updated = self.update_by_document_id(
                document_id,
                status=status,
                ocr_text=ocr_text,
                table_data=table_data,
                error_message=error_message,
            )
            if updated is None:
                raise RuntimeError("OCRResult upsert failed unexpectedly.")
            return updated

        return self.create(
            document_id=document_id,
            status=status,
            ocr_text=ocr_text,
            table_data=table_data,
            error_message=error_message,
        )

    def mark_processing(self, document_id: UUID) -> OCRResult:
        """
        Create if not exists, otherwise set status back to processing.
        """
        return self.upsert_by_document_id(
            document_id,
            status=OCRStatus.PROCESSING,
            ocr_text="",
            table_data=None,
            error_message=None,
        )

    def mark_completed(
        self,
        document_id: UUID,
        *,
        ocr_text: str,
        table_data: Optional[Dict[str, Any]] = None,
    ) -> OCRResult:
        return self.upsert_by_document_id(
            document_id,
            status=OCRStatus.SUCCESS,
            ocr_text=ocr_text,
            table_data=table_data,
            error_message=None,
        )

    def mark_failed(
        self,
        document_id: UUID,
        *,
        error_message: str,
    ) -> OCRResult:
        return self.upsert_by_document_id(
            document_id,
            status=OCRStatus.FAILED,
            ocr_text="",
            table_data=None,
            error_message=error_message,
        )