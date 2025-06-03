from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.schemas.user import UserLogin
from fastapi.responses import JSONResponse
from src.db.queries import get_user_by_email
from src.api.utils.auth import create_access_token
from src.core.exceptions import credentials_exception
from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class BaseUserService:
    @staticmethod
    def login(user_data: UserLogin, db: Session) -> JSONResponse:
        user = get_user_by_email(user_data.email, db)

        if not user or not pwd_context.verify(user_data.password, user.hashed_password):
            raise credentials_exception()
        
        token = create_access_token({"sub": user.email})
        resp = JSONResponse({"message": "Access granted"})
        
        resp.set_cookie(
                            key="authorization",
                            value=token,
                            httponly=True,
                            secure=True,
                            samesite="none",
                            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60,
                            path="/"
                        )

        return resp
    
    @staticmethod
    def logout() -> JSONResponse:
        response = JSONResponse({"message": "Goodbye"})
        response.delete_cookie("authorization")
        return response