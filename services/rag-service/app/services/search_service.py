# app/services/search_service.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.db.session import session_scope
from app.repositories.chunk_repository import ChunkRepository
from app.services.embedding_service import EmbeddingService
from app.vectorstore.chroma_repo import ChromaVectorRepository, VectorHit


@dataclass
class SearchHit:
    chunk_id: str
    distance: float
    text: str
    document_id: str
    chunk_index: int
    start_offset: Optional[int]
    end_offset: Optional[int]
    metadata: Dict[str, Any]


class SearchService:
    """
    Semantic search service:
    query text -> embed -> vector search (Chroma) -> map back to chunks in Postgres (source of truth).

    Notes:
    - Chroma stores embeddings + metadata as an index layer.
    - Postgres stores chunk truth data (text, offsets, etc).
    """

    def __init__(
        self,
        *,
        embedding_service: EmbeddingService,
        vector_repo: ChromaVectorRepository,
    ):
        self.embedding_service = embedding_service
        self.vector_repo = vector_repo

    def search(
        self,
        *,
        query: str,
        top_k: int = 5,
        document_id: Optional[str] = None,
    ) -> List[SearchHit]:
        q = (query or "").strip()
        if not q:
            return []

        # 1) embed query (no DB session)
        query_vec = self.embedding_service.embed_text(q)
        print(f"Searching with document_id: {document_id}")
        print(f"Query embedding: {query_vec}")

        # 2) vector search (index layer)
        hits: List[VectorHit] = self.vector_repo.query(
            query_embedding=query_vec,
            top_k=top_k,
            document_id=document_id,
        )

        # 3) extract chunk_ids from hits (prefer metadata["chunk_id"], fallback to hit.id)
        chunk_ids: List[str] = []
        for h in hits:
            cid = h.metadata.get("chunk_id") or h.id
            if cid:
                chunk_ids.append(str(cid))

        if not chunk_ids:
            return []

        # 4) fetch chunks from Postgres (source of truth)
        with session_scope() as db:
            chunk_repo = ChunkRepository(db)
            chunks = chunk_repo.get_by_ids(chunk_ids)

            for chunk in chunks:
                db.refresh(chunk)

            chunk_map = {str(c.id): c for c in chunks}

            # 5) assemble response in the same order as vector hits
            results: List[SearchHit] = []
            
            for h in hits:
                cid = str(h.metadata.get("chunk_id") or h.id)
                c = chunk_map.get(cid)

                # If missing in DB, fallback to Chroma stored "document" field
                text = c.text if c is not None else (h.document or "")

                # metadata fields (may be absent depending on exclude_none)
                doc_id = ""
                chunk_index = -1
                start_offset = None
                end_offset = None

                if c is not None:
                    doc_id = str(c.document_id)
                    chunk_index = int(c.chunk_index)
                    start_offset = c.start_offset
                    end_offset = c.end_offset
                else:
                    doc_id = str(h.metadata.get("document_id") or "")
                    chunk_index = int(h.metadata.get("chunk_index") or -1)
                    # offsets might not exist in metadata if you excluded None; handle safely
                    so = h.metadata.get("start_offset")
                    eo = h.metadata.get("end_offset")
                    start_offset = int(so) if isinstance(so, int) else None
                    end_offset = int(eo) if isinstance(eo, int) else None

                results.append(
                    SearchHit(
                        chunk_id=cid,
                        distance=float(h.distance),
                        text=text,
                        document_id=doc_id,
                        chunk_index=chunk_index,
                        start_offset=start_offset,
                        end_offset=end_offset,
                        metadata=h.metadata,
                    )
                )

            return results
