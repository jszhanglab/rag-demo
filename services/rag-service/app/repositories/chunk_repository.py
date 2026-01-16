# app/repositories/chunk_repository.py
from typing import Any, Dict, List
from sqlalchemy import insert, delete
from app.db.models.chunk import Chunk
from sqlalchemy.orm import Session

class ChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_chunk(self, session: Session, chunk_data: dict) -> None:
        chunk = Chunk(
            document_id=chunk_data["document_id"],
            chunk_index=chunk_data["chunk_index"],
            start_offset=chunk_data["start_offset"],
            end_offset=chunk_data["end_offset"],
            token_count=chunk_data["token_count"],
            text=chunk_data["text"],
            embedding_id=chunk_data["embedding_id"]
        )
        session.add(chunk)
        session.commit()

    def list_by_document_id(self, document_id: str) -> List[Chunk]:
        return (
            self.db.query(Chunk)
            .filter(Chunk.document_id == document_id)
            .order_by(Chunk.chunk_index.asc())
            .all()
        )    
        
    def bulk_insert(self, chunk_records: List[Dict[str, Any]]) -> None:
        if not chunk_records:
            return

        try:
            self.db.execute(
                insert(Chunk),
                chunk_records
            )
        except Exception as e:
            raise e

    def delete_by_document_id(self, document_id: str) -> None:
        self.db.execute(
            delete(Chunk).where(Chunk.document_id == document_id)
        )    