from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .utils.config import API_ROUTES

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_PATH = API_ROUTES['UPLOAD_DOCUMENT']

@app.post(UPLOAD_PATH)
def test():
    return{"status": "ok", "service": "rag-service", "message": "FastAPI is alive!"}