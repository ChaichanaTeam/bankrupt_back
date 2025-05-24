from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src.db.session import engine
from src.db.base import Base
from src.api.routes import user as user_routes
# from src.api.routes import wallet as wallet_routes
from src.api.routes import cleanup as jobs_routes
from src.api.routes import cards as card_routes
from src.api.routes import admin as admin_routes
from src.api.routes import savings as savings_routes
from typing import AsyncGenerator, Any

# async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any, None]:
    
#     yield

class BackendApp(FastAPI):
    def __init__(self):
        super().__init__()
        super().add_middleware(
            CORSMiddleware,
            allow_origins=["*"], #settings.ORIGINS
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        Base.metadata.create_all(bind=engine)
        super().mount("/static", StaticFiles(directory="src/static"), name="static")
        self.__initializeRoutes(super())

    def __initializeRoutes(self, app: FastAPI) -> None:
        app.include_router(user_routes.router, prefix="/auth", tags=["auth"])
        # app.include_router(wallet_routes.router, prefix="/account", tags=["account"])
        app.include_router(jobs_routes.router, tags=["miscallenious"])
        app.include_router(card_routes.router, prefix="/card", tags=["card"])
        app.include_router(admin_routes.router, prefix="/admin", tags=["admin"])
        app.include_router(savings_routes.router, prefix="/savings", tags=["savings"])

        @self.get("/")
        def read_root():
            return {"Status": "Server up and running"}