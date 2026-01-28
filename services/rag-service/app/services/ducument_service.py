#app\services\ducument_service.py
from sqlalchemy.orm import Session
from app.repositories.document_repository import DocumentRepository

def get_document_list(db:Session,user_id:str) -> list:
    repo = DocumentRepository(db)
    return repo.get_by_user_id(user_id)


def mark_status(db:Session,status:str):
    repo = DocumentRepository(db)
    repo.update_document()
    return

def get_document_detail(db:Session,document_id:str):
    repo = DocumentRepository(db)
    return repo.get_by_id(document_id)
