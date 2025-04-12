from fastapi import FastAPI

from src.db.session import engine
from src.models import user, wallet
from src.db.base import Base
from src.api.routes import user as user_routes

app: FastAPI = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root() -> None:
    return {"message": "Бекенд банковского приложения работает!"}

app.include_router(user_routes.router, prefix="/auth", tags=["auth"])

# def init() -> None:

# if __name__ == "__main__":
#     init()