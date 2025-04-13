import os

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()