# app/vectorstore/chroma_repo.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, List

import chromadb
from chromadb.api.models.Collection import Collection

from app.vectorstore.schemas import ChunkVectorMeta


@dataclass
class VectorHit:
    id: str
    distance: float
    document: Optional[str]
    metadata: dict[str, Any]


class ChromaVectorRepository:
    """
    A thin wrapper over Chroma.
    - Keep Postgres as source of truth.
    - Treat Chroma as rebuildable index.
    """

    def __init__(self, persist_dir: str, collection_name: str):
        self._client = chromadb.PersistentClient(path=persist_dir)
        self._collection: Collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},  # cosine/l2
        )

    @property
    def collection(self) -> Collection:
        return self._collection

    def upsert_chunks(
        self,
        *,
        chunk_ids: List[str],
        embeddings: List[list[float]],
        documents: List[str],
        metadatas: List[ChunkVectorMeta],
    ) -> None:
        """
        Note: Chroma behavior differs by version.
        Safe approach: delete existing ids then add.
        """
        ids = [str(x) for x in chunk_ids]
        metas = [m.model_dump(exclude_none=True) for m in metadatas]

        # delete existing (ignore if not exists)
        try:
            self._collection.delete(ids=ids)
        except Exception:
            # some versions may throw if ids not found; ignoring is OK for index layer
            pass

        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metas,
        )

    def query(
        self,
        *,
        query_embedding: list[float],
        top_k: int = 5,
        document_id: Optional[str] = None,
    ) -> List[VectorHit]:
        where = {"document_id": document_id} if document_id else None

        res = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
            include=["metadatas", "documents", "distances"],
        )

        # Chroma returns lists per query (we pass one query)
        ids = (res.get("ids") or [[]])[0]
        dists = (res.get("distances") or [[]])[0]
        docs = (res.get("documents") or [[]])[0]
        metas = (res.get("metadatas") or [[]])[0]

        hits: List[VectorHit] = []
        for i, _id in enumerate(ids):
            hits.append(
                VectorHit(
                    id=_id,
                    distance=float(dists[i]) if dists and i < len(dists) else 0.0,
                    document=docs[i] if docs and i < len(docs) else None,
                    metadata=metas[i] if metas and i < len(metas) else {},
                )
            )
        return hits

    def delete_by_document(self, document_id: str) -> None:
        """
        Delete all vectors belonging to a document.
        """
        self._collection.delete(where={"document_id": document_id})
