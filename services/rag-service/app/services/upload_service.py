from pathlib import Path
import shutil
import os
from fastapi import UploadFile

UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploaded_files"

# make directory if is not exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(file: UploadFile):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        return {"status": "success", "filename": file.filename, "message": "File uploaded successfully!"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
