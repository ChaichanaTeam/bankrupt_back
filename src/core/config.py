import os
from pathlib import Path
from dotenv import load_dotenv

env_path: Path = Path(__file__).resolve().parents[2] / ".env" / "var.env"

if env_path.exists():
    print(".env loaded")
    load_dotenv(dotenv_path=env_path)
else:
    print(".env not loaded, using os variables if exists. Check for variables if errors are raised")
    

class Settings:
    DATABASE_URL: str = "sqlite:///./bank.db"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMAIL: str = os.getenv("EMAIL")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    IS_DEPLOYED = os.getenv("DEPLOY") is not None

settings = Settings()