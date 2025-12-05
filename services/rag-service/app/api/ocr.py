from fastapi import APIRouter
from pydantic import BaseModel

from ..services.ocr_service import run_ocr

router = APIRouter()

class OCRRequest(BaseModel):
    file_key: str

@router.post("/ocr")
async def ocr_endpoint(request: OCRRequest):
    text = await run_ocr(request.file_key)
    return {"text": text}
