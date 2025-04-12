from fastapi import FastAPI

from src.db.session import engine
from src.models import user
from src.db.base import Base

app: FastAPI = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Бекенд банковского приложения работает!"}