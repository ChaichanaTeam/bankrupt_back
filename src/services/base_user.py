from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.schemas.user import UserLogin
from src.db.queries import get_user_by_email
from src.api.utils.auth import create_access_token
from src.core.exceptions import credentials_exception

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class BaseUserService:
    @staticmethod
    def login(user_data: UserLogin, db: Session) -> str:
        user = get_user_by_email(user_data.email, db)

        if not user or not pwd_context.verify(user_data.password, user.hashed_password):
            raise credentials_exception()

        return create_access_token({"sub": user.email})