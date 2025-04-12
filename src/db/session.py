from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./bank.db"

engine: Engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)