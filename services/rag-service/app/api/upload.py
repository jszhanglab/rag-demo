# rag-service/app/api/upload.py

from fastapi import APIRouter, File, UploadFile
from ..utils.config import API_ROUTES
from ..services.upload_service import save_uploaded_file

# APIRouter allows splitting API endpoints into modular components.
router = APIRouter()

@router.post(API_ROUTES['UPLOAD_DOCUMENT'])
async def upload_file(file: UploadFile = File(...)):
    result = save_uploaded_file(file)
    return result
    