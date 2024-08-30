"""Connecting to Postgres"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DBSession = sessionmaker()

load_dotenv()

user = os.getenv("POSTGRES_USER")
passwd = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
dbname = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{user}:{passwd}@{host}:{port}/{dbname}"

engine = create_engine(
    url=DATABASE_URL,
    echo=False
)
session = DBSession(bind=engine)
Base = declarative_base()
