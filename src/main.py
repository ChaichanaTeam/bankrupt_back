from fastapi import FastAPI
from src.db.session import engine
from src.db.base import Base
from src.api.routes import user as user_routes
from src.api.routes import wallet as wallet_routes
from src.api.routes import cleanup as jobs_routes
from fastapi.middleware.cors import CORSMiddleware

app: FastAPI = FastAPI()

origins = [
    "http://localhost:5173",          # Vite локально
    "http://127.0.0.1:5173",
    # Можешь добавить и прод-фронт:
    # "https://your-frontend.web.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Или ["*"] — на время разработки
    allow_credentials=True,
    allow_methods=["*"],          # Или ['POST', 'GET']
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Status": "Server up and running"}

app.include_router(user_routes.router, prefix="/auth", tags=["auth"])
app.include_router(wallet_routes.router, prefix="/account", tags=["account"])
app.include_router(jobs_routes.router, tags=["miscallenious"])