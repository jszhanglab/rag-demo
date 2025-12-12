# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path

DOTENV_PATH = Path(__file__).resolve().parent.parent / 'config' / '.env'

load_dotenv(dotenv_path=DOTENV_PATH)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_DEV")

# create a connection with db
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
