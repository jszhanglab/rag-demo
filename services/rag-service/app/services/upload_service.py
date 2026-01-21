from pathlib import Path
import shutil
import os
from fastapi import UploadFile,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.document_repository import DocumentRepository
from app.constants.status import DocumentStatus
from uuid import UUID

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploaded_files"

# make directory if is not exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(file: UploadFile,db: Session,user_id: UUID,source: str):
    try:
        # Step 1: Save file to the storage
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Step 2:Save file metadata to db
        document_repo = DocumentRepository(db)
        db_document = document_repo.create_document(
            user_id = user_id,
            filename = file.filename,
            file_path = file_location,
            mime_type = file.content_type,  # MIME type of the uploaded file
            file_size_bytes = file.size,    # Size of the uploaded file
            source = source,                 # Source can be 'upload', 'api', or 'url'
            status = DocumentStatus.UPLOADED
        )
        
        return {"document_status": db_document.status, "filename": file.filename, "document_id": db_document.id}
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database operation failed: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="File upload failed: " + str(e))
