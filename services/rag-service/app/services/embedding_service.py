# app/services/embedding_service.py

from __future__ import annotations

from typing import List, Optional
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Local embedding service using Sentence-Transformers.

    Responsibilities:
    - Load embedding model (lazy)
    - Provide embed_text / embed_texts
    - Keep it independent from DB / VectorStore
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        normalize: bool = True,
        batch_size: int = 32,
        device: Optional[str] = None,  # e.g. "cpu" or "cuda"
    ):
        self.model_name = model_name
        self.normalize = normalize
        self.batch_size = batch_size
        self.device = device

        self._model: Optional[SentenceTransformer] = None

    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            # SentenceTransformer can auto-pick device if device is None
            self._model = SentenceTransformer(self.model_name, device=self.device)
        return self._model

    def embed_text(self, text: str) -> List[float]:
        vectors = self.embed_texts([text])
        return vectors[0]

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        # Basic input hygiene
        cleaned = [(t or "").strip() for t in texts]
        model = self._get_model()

        # Returns numpy array; convert to plain python lists for Chroma
        emb = model.encode(
            cleaned,
            batch_size=self.batch_size,
            normalize_embeddings=self.normalize,
            show_progress_bar=False,
        )
        return emb.tolist()
