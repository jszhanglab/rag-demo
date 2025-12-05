from paddleocr import PaddleOCR
import os

OCR_ENGINES = {
    "ja": PaddleOCR(lang="japan"),
    "zh": PaddleOCR(lang="ch"),
    "en": PaddleOCR(lang="en"),
    #"multi": PaddleOCR(lang="multilingual")
}

def get_ocr_engine(lang):
    return OCR_ENGINES.get(lang, OCR_ENGINES["en"])

async def run_ocr(file_path: str) -> str:
    if not os.path.exists(file_path):
        return "File not found"

    result = get_ocr_engine.ocr(file_path)
    text = "\n".join([line[1][0] for line in result[0]])
    return text
