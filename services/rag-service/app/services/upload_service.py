from pathlib import Path
import shutil
import os
from fastapi import UploadFile,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.document_repository import DocumentRepository
from uuid import UUID

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploaded_files"

# make directory if is not exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Upload success mock
MOCK_USER_ID = UUID('00000000-0000-0000-0000-000000000001')

# TODO Upload fail mock
MOCK_USER_ID_FAIL = UUID('10000000-0000-0000-0000-000000000001')

def save_uploaded_file(file: UploadFile,db: Session,user_id: UUID,source: str):
    try:
        # Step 1: Save file to the storage
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Step 2:Save file metadata to db
        document_repo = DocumentRepository(db)
        db_document = document_repo.create_document(
            user_id=MOCK_USER_ID_FAIL,
            filename=file.filename,
            mime_type=file.content_type,  # MIME type of the uploaded file
            file_size_bytes=file.size,    # Size of the uploaded file
            source=source                 # Source can be 'upload', 'api', or 'url'
        )
        
        return {"status": "success", "filename": file.filename, "document_id": db_document.id,"message": "File uploaded successfully!"}
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database operation failed: " + str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="File upload failed: " + str(e))
