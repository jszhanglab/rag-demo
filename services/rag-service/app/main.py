from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .utils.config import settings
from .api.upload import router as upload_router
from .api.ocr import router as ocr_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    #lifespan=lifespan
)

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