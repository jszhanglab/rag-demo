# app/vectorstore/schemas.py

from pydantic import BaseModel, Field
from typing import Optional, Literal


class ChunkVectorMeta(BaseModel):
    schema_ver: Literal["1"] = "1"

    document_id: str = Field(..., description="Source document UUID")
    chunk_id: str = Field(..., description="Chunk UUID (primary link key)")
    chunk_index: int = Field(..., description="Order of chunk in document")

    source: Literal["ocr", "raw_text"] = "ocr"

    # text-based positioning
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None

    # page-based positioning (PDF / OCR)
    page: Optional[int] = None

    class Config:
        extra = "forbid"
