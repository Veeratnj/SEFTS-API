import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv, find_dotenv


SQLITE_DATABASE_URL = "sqlite:///./app/db/E-com.db"
engine=create_engine(SQLITE_DATABASE_URL)
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()