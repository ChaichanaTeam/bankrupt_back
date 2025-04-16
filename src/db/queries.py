from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from sqlalchemy import exists
from src.schemas.user import UserCreate, UserLogin
from src.schemas.token import Token
from src.models.wallet import Wallet
from src.models.user import User, UserTemp as UnverifiedUser

def is_user_existing(user: UserCreate, db: Session) -> bool:
    return db.query(exists().where(
        (User.email == user.email) |
        (User.social_security == user.social_security) |
        (User.phone_number == user.phone_number)
    )).scalar()

def get_expired_users(threshold: datetime, db: Session) -> list[UnverifiedUser]:
    return db.query(UnverifiedUser).filter(UnverifiedUser.created_at < threshold).all()

def get_unverified_user(email: str, db: Session) -> UnverifiedUser:
    return db.query(UnverifiedUser).filter(User.email == email).first()

def get_user(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

def is_code_valid(email: str, code: str, db: Session) -> bool:
    return db.query(exists().where(
        (UnverifiedUser.email == email) &
        (UnverifiedUser.code == code)
    )).scalar()