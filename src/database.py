# db connection related stuff

import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import database_settings

logging.basicConfig()

if database_settings.enable_sqlite:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    connect_args = {"check_same_thread": False}
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
else:
    SQLALCHEMY_DATABASE_URL = f"postgresql://{database_settings.username}:{database_settings.password.get_secret_value()}@{database_settings.hostname}/{database_settings.database}"
    connect_args = {}
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARN)
    
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args=connect_args # check_same_thread to False for SQLite only
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
