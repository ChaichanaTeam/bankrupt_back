from types import NoneType
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.schemas.user import UserCreate, UserLogin, UserTemp
from src.models.user import User, UnverifiedUser
from src.db.queries import get_expired_users
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
        except Exception as e:
            print(e)
            raise credentials_exception()
            
        return BaseUserService.login(user_data, db)
    
    @staticmethod
    def validate(admin: User | str) -> None:
        reason: str = "Invalid Credentials"
        if isinstance(admin, str):
            reason = admin
            raise credentials_exception(reason)
        
        if isinstance(admin, User):
            if not (admin and admin.is_superuser):
                raise credentials_exception(reason)
            
    @staticmethod
    def cleanup_users(db: Session) -> int:
        expired_users = get_expired_users(db)
        deleted_count: int = len(expired_users)

        for user in expired_users:
            db.delete(user)
        db.commit()

        return deleted_count