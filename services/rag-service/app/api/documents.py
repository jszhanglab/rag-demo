# rag-service/app/api/documents.py

from fastapi import APIRouter, Depends, UploadFile
from app.utils.config import API_ROUTES
from app.services.ducument_service import get_document_list,get_document_detail
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.utils.mock.mock_user import get_current_user

# APIRouter allows splitting API endpoints into modular components.
router = APIRouter()

@router.get(API_ROUTES['GET_FILE_LIST'])
async def document_list(db: Session = Depends(get_db)):
    mock_user_id = get_current_user()
    document_list = get_document_list(db, mock_user_id)
    return {"document_list": document_list}

@router.get(API_ROUTES['GET_DOCUMENT_DETAIL'])
async def document_detail(document_id: str, db: Session = Depends(get_db)):
    doc = get_document_detail(db, document_id)
    return doc