# rag-service/app/api/upload.py

from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, BackgroundTasks
from app.utils.config import API_ROUTES
from app.services.upload_service import save_uploaded_file
from app.pipelines.document_pipeline import process_document_pipeline
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.utils.mock.mock_user import get_current_user

# APIRouter allows splitting API endpoints into modular components.
router = APIRouter()

@router.post(API_ROUTES['UPLOAD_DOCUMENT'])
async def upload_file(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session= Depends(get_db),
    source: str = "upload"
):
    mock_user_id = get_current_user()
    result = save_uploaded_file(file,db,mock_user_id,source)
    document_id=result["document_id"]
    # TODO:Determine source file language dynamically (currently hardcoded to "en")

    # Since a UUID is a reference type, it is not JSON-serializable by default.
    # Converting to string ensures compatibility with task queues (like Celery/Redis) 
    # if we scale to a distributed architecture later.
    background_tasks.add_task(process_document_pipeline, str(document_id), "en")
    return result
    