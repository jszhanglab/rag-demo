# app/db/base.py
from sqlalchemy.orm import declarative_base

#Base is the ORM base class from which all declarative models extend.
Base = declarative_base()