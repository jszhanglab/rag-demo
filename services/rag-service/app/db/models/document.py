# app/db/models/document.py

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)  # document owner
    filename = Column(String(255), nullable=False)
    file_path = Column(String, nullable=False)
    mime_type = Column(String(100))
    file_size_bytes = Column(Integer)
    status = Column(String(50), nullable=False)  # uploaded | processing | ready | failed
    error_message = Column(String)
    source = Column(String(50), nullable=False)  # upload | api | url
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    updated_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    deleted_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id], back_populates="documents")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], backref="created_documents")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], backref="updated_documents")
    deleted_by_user = relationship("User", foreign_keys=[deleted_by_user_id], backref="deleted_documents")

    ocr_result = relationship(
        "OCRResult",
        back_populates="document",
        uselist=False,
        cascade="all, delete-orphan",
    )