from enum import Enum

class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    OCR_PROCESSING = "OCR_PROCESSING"
    OCR_DONE = "OCR_DONE"
    CHUNK_DONE = "CHUNK_DONE"
    EMBEDDING_DONE = "EMBEDDING_DONE"
    FAILED = "FAILED"

class OCRStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
