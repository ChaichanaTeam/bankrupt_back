from fastapi import FastAPI

from src.db.session import engine
from src.models import user, wallet
from src.db.base import Base
from src.api.routes import user as user_routes
from src.api.routes import wallet as wallet_routes

app: FastAPI = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Бекенд банковского приложения работает!"}

app.include_router(user_routes.router, prefix="/auth", tags=["auth"])
app.include_router(wallet_routes.router, prefix="/account", tags=["account"])