import os
from pathlib import Path
from dotenv import load_dotenv

env_path: Path = Path(__file__).resolve().parents[2] / ".env" / "var.env"

if env_path.exists():
    load_dotenv(dotenv_path=env_path)

class Settings:
    DATABASE_URL: str = "sqlite:///./bank.db"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMAIL: str = os.getenv("EMAIL")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    IS_DEPLOYED = os.getenv("DEPLOY") is not None

settings = Settings()