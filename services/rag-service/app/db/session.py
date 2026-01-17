# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path
from contextlib import contextmanager
from app.utils.config import get_dotenv_path
from app.utils.config import settings

DOTENV_PATH = get_dotenv_path()

load_dotenv(dotenv_path=DOTENV_PATH)
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL_DEV

# create a connection with db
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Used by FastAPI, lifecycle is one single Http request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @contextmanager transforms a generator function into a Context Manager object. 
# This object automatically implements the __enter__() and __exit__() methods, 
# allowing the function to be used with the 'with' statement.
@contextmanager
# Used by background tasks.
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
