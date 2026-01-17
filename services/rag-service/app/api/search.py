# app/api/search.py

from fastapi import APIRouter
from app.utils.config import API_ROUTES
from app.utils.config import settings
from app.services.search_service import SearchService
from app.services.embedding_service import EmbeddingService
from app.vectorstore.chroma_repo import ChromaVectorRepository
from pydantic import BaseModel, Field
from typing import List, Optional
import os

router = APIRouter(prefix=API_ROUTES['SEARCH_DOCUMENT'], tags=["search"])
VECTOR_DB_URL = settings.VECTOR_DB_URL
LLM_MODEL_DEV = settings.LLM_MODEL_DEV

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Search query text")
    top_k: int = Field(5, ge=1, le=50, description="Number of results to return")
    document_id: Optional[str] = Field(None, description="Optional document_id filter (UUID string)")

class SearchHitResponse(BaseModel):
    chunk_id: str
    distance: float
    text: str
    document_id: str
    chunk_index: int
    start_offset: Optional[int] = None
    end_offset: Optional[int] = None
    metadata: dict

class SearchResponse(BaseModel):
    hits: List[SearchHitResponse]

# Initialize services (you can use dependency injection in a more complex setup)
embedding_service = EmbeddingService(
    model_name=LLM_MODEL_DEV,
    normalize=True,
    batch_size=32,
    device=None,
)

vector_repo = ChromaVectorRepository(
    persist_dir=VECTOR_DB_URL,
    collection_name="rag_chunks", #TODO
)

search_service = SearchService(
    embedding_service=embedding_service,
    vector_repo=vector_repo,
)

# Create an APIRouter instance for the search endpoint
@router.post("", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Endpoint to search the vector database and retrieve relevant chunks.
    """
    # Call the search service to get the results
    hits = search_service.search(query=request.query, top_k=request.top_k, document_id=request.document_id)

    # Return the search results
    return SearchResponse(
        hits=[
            SearchHitResponse(
                chunk_id=hit.chunk_id,
                distance=hit.distance,
                text=hit.text,
                document_id=hit.document_id,
                chunk_index=hit.chunk_index,
                start_offset=hit.start_offset,
                end_offset=hit.end_offset,
                metadata=hit.metadata
            )
            for hit in hits
        ]
    )
