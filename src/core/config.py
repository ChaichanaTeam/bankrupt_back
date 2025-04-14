import os

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    EMAIL: str = os.getenv("EMAIL")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")
    IS_DEPLOYED = os.getenv("DEPLOY") is not None

settings = Settings()