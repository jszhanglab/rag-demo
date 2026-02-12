# app/repositories/document_repository.py

from sqlalchemy import func, update
from sqlalchemy.orm import Session,joinedload
from app.db.models.user import User
from app.db.models.document import Document
from uuid import UUID
from typing import List, Optional


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(
            self, 
            user_id: UUID, 
            filename: str, 
            file_path: str, 
            mime_type: str, 
            file_size_bytes: int, 
            source: str,status:str
        ) -> Document:
        db_document = Document(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            mime_type=mime_type,
            file_size_bytes=file_size_bytes,
            status=status,
            source=source
        )
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def get_by_id(self, document_id: UUID) -> Optional[Document]:
        return self.db.query(Document)\
            .options(joinedload(Document.ocr_result))\
            .filter(Document.id == document_id)\
            .first()

    def get_by_user_id(self, user_id: UUID) -> List[Document]:
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
    
    # def mark_status(self, document_id: UUID, status: str):
    #     db_document = self.db.query(Document).filter(Document.id == document_id).first()
    #     if db_document:
    #        db_document.status = status
    #        self.db.commit()
    #        self.db.refresh(db_document)
    #        return db_document
    #     return

    def mark_status(self, document_id: UUID, status: str):
        self.db.execute(
            update(Document)
            .where(Document.id == document_id)
            .values(status=status)
        )   


