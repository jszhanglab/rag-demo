# app/services/ocr_service.py
from __future__ import annotations

import os
import threading
from typing import Dict
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

from paddleocr import PaddleOCR

from app.repositories.ocr_result_repository import OCRResultRepository
from app.repositories.document_repository import DocumentRepository
from app.constants.status import OCRStatus

_LANG_MAP = {
    "ja": "japan",
    "zh": "ch",
    "en": "en",
}

# Lazy load
_OCR_ENGINES: Dict[str, PaddleOCR] = {}
_LOCK = threading.Lock()


def get_ocr_engine(lang: str) -> PaddleOCR:
    """
    Lazily create and cache PaddleOCR engine per language.
    Thread-safe for single-process multi-thread usage.
    """
    key = (lang or "en")
    paddle_lang = _LANG_MAP.get(key, _LANG_MAP["en"])

    engine = _OCR_ENGINES.get(paddle_lang)
    if engine is not None:
        return engine

    with _LOCK:
        engine = _OCR_ENGINES.get(paddle_lang)
        if engine is None:
            engine = PaddleOCR(lang=paddle_lang)
            _OCR_ENGINES[paddle_lang] = engine
        return engine


def run_ocr(file_path: str, lang: str = "en") -> str:
    """
    Run OCR and return extracted text.
    Keep this function "pure-ish": it returns text and raises on fatal errors.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    engine = get_ocr_engine(lang)

    result = engine.ocr(file_path)

    lines = []
    for page_idx, page in enumerate(result or []):
        lines.append(f"\n--- Page {page_idx + 1} ---\n")
        for line in page:
            lines.append(line[1][0])

    return "\n".join(lines)
