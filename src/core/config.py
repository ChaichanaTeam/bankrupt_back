import os
from pathlib import Path
from dotenv import load_dotenv

env_path: Path = Path(__file__).resolve().parents[2] / ".env" / "var.env"

def print_info(text: str) -> None:
    print(f"\033[32mINFO:\033[0m {text}")

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
    print_info(".env loaded")
else:
    print_info(".env not loaded, using os variables if exists. Check for variables if errors are raised")
    

class Settings:
    def __init__(self):
        self.DATABASE_URL: str = "sqlite:///./bank.db"
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-key")
        self.ALGORITHM: str = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
        self.EMAIL: str = os.getenv("EMAIL")
        self.EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
        self.IS_DEPLOYED = os.getenv("DEPLOY") is not None
        self.ORIGINS = self._get_origins()
        print_info(f"Loaded origins {self.ORIGINS}")
    
    def _get_origins(self):
        origins = []
        if os.getenv("DEBUG") is not None:
            origins.append("http://localhost:5173")
            origins.append("http://127.0.0.1:5173")
        frontend = os.getenv("FRONTEND_LINK")
        if frontend:
            origins.append(frontend)
        return origins

settings = Settings()