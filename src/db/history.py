from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

HISTORY_DATABASE_URL = "sqlite:///./bank_history.db"

engine_history = create_engine(
    HISTORY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocalHistory = sessionmaker(autocommit=False, autoflush=False, bind=engine_history)

BaseHistory = declarative_base()
