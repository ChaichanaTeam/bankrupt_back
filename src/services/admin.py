from types import NoneType
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.schemas.user import UserCreate, UserLogin, UserTemp
from src.models.user import User, UnverifiedUser
from src.models.wallet import Wallet
from src.db.queries import is_superuser, get_user_by_email
from src.api.utils.auth import create_access_token, create_verification_code, get_current_user_cookie
from src.api.utils.mail import send_verification_email
from src.core.exceptions import credentials_exception
from src.services.base_user import BaseUserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdminService(BaseUserService):
    @staticmethod
    def login(user_data: UserLogin, db: Session) -> str:
        try:
            if not is_superuser(get_user_by_email(user_data.email, db).id, db):
                raise credentials_exception()
        except Exception:
            raise credentials_exception()
            
        return BaseUserService.login(user_data, db)
    
    @staticmethod
    def validate(token: str, db: Session):
        if not token:
            raise credentials_exception()

        current_user: User = get_current_user_cookie(token, db)

        return current_user