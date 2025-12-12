# app/repositories/document_repository.py

from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.models.user import User
from app.db.models.document import Document
from uuid import UUID
from typing import List, Optional


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, user_id: UUID, filename: str, mime_type: str, file_size_bytes: int, source: str) -> Document:
        db_document = Document(
            user_id=user_id,
            filename=filename,
            mime_type=mime_type,
            file_size_bytes=file_size_bytes,
            status="uploaded",
            source=source
        )
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def get_document_by_id(self, document_id: UUID) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_documents_by_user_id(self, user_id: UUID) -> List[Document]:
        return self.db.query(Document).filter(Document.user_id == user_id).all()

    def update_document(self, document_id: UUID, status: str, error_message: Optional[str] = None) -> Optional[Document]:
        db_document = self.db.query(Document).filter(Document.id == document_id).first()
        if db_document:
            db_document.status = status
            db_document.error_message = error_message
            self.db.commit()
            self.db.refresh(db_document)
            return db_document
        return None

    def delete_document(self, document_id: UUID) -> bool:
        db_document = self.db.query(Document).filter(Document.id == document_id).first()
        if db_document:
            db_document.deleted_at = func.now()
            self.db.commit()
            return True
        return False
