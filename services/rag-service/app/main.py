# app/main.py
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .utils.config import settings
from .api.upload import router as upload_router
from .api.ocr import router as ocr_router
from .api.documents import router as get_documents_router
from .api.search import router as search_router

is_dev = settings.ENV.lower() in ("dev", "develop", "development")
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    docs_url="/docs" if is_dev else None,
    redoc_url="/redoc" if is_dev else None,
    openapi_url="/openapi.json" if is_dev else None,
    #lifespan=lifespan
)

#TODO A temporary way to load PDF in local dev enviroment.
# Can not be used on cloud storage likes S3. 
UPLOAD_DIR = r"C:\Users\zhang\Desktop\RAG\rag_demo\services\rag-service\app\uploaded_files"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")    

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include_router is used for integrating different api module into the main FastAPI application.
app.include_router(upload_router)
app.include_router(ocr_router)
app.include_router(get_documents_router)
app.include_router(search_router)