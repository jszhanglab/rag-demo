# app/services/ocr_service.py
from __future__ import annotations

import os
import threading
from typing import Dict, List, Any
from paddleocr import PaddleOCR

_LANG_MAP = {
    "ja": "japan",
    "zh": "ch",
    "en": "en",
}

_OCR_ENGINES: Dict[str, PaddleOCR] = {}
_LOCK = threading.Lock()

def get_ocr_engine(lang: str) -> PaddleOCR:
    key = (lang or "en")
    paddle_lang = _LANG_MAP.get(key, _LANG_MAP["en"])

    engine = _OCR_ENGINES.get(paddle_lang)
    if engine is not None:
        return engine

    with _LOCK:
        engine = _OCR_ENGINES.get(paddle_lang)
        if engine is None:
            engine = PaddleOCR(lang=paddle_lang, use_angle_cls=True, show_log=False)
            _OCR_ENGINES[paddle_lang] = engine
        return engine

def run_ocr(file_path: str, lang: str = "en") -> List[Dict[str, Any]]:
    """
    Run OCR and return a list of structured data instead of raw text.
    Each item contains: text, page_index, and bounding box coordinates.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    engine = get_ocr_engine(lang)
    result = engine.ocr(file_path)

    structured_results = []

    for page_idx, page in enumerate(result or []):
        if page is None:
            continue
        
        for line in page:

            box = line[0]
            text_content = line[1][0]
            
            structured_results.append({
                "text": text_content,
                "page": page_idx + 1, 
                "bbox": box,          
                "y_center": (box[0][1] + box[2][1]) / 2 
            })

    return structured_results