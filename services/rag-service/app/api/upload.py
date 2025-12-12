# rag-service/app/api/upload.py

from fastapi import APIRouter, Depends, UploadFile
from app.utils.config import API_ROUTES
from app.services.upload_service import save_uploaded_file
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.utils.mock.mock_user import get_current_user

# APIRouter allows splitting API endpoints into modular components.
router = APIRouter()

@router.post(API_ROUTES['UPLOAD_DOCUMENT'])
async def upload_file(file: UploadFile,db: Session= Depends(get_db),source: str = "upload"):
    mock_user_id = get_current_user()
    result = save_uploaded_file(file,db,mock_user_id,source)
    return result
    