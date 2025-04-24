from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from sqlalchemy import exists
from src.schemas.user import UserCreate, UserLogin
from src.schemas.token import Token
from src.models.wallet import Wallet
from src.models.wallet_history import TransferHistory
from src.models.cards import Card
from src.models.user import User, UnverifiedUser 

def is_user_existing(user: UserCreate, db: Session) -> bool:
    return db.query(exists().where(
        (User.email == user.email) |
        (User.social_security == user.social_security) |
        (User.phone_number == user.phone_number)
    )).scalar() or \
    db.query(exists().where(
        (UnverifiedUser.email == user.email) |
        (UnverifiedUser.social_security == user.social_security) |
        (UnverifiedUser.phone_number == user.phone_number)
    )).scalar()

def get_expired_users(threshold: datetime, db: Session) -> list[UnverifiedUser]:
    return db.query(UnverifiedUser).filter(UnverifiedUser.created_at < threshold).all()

def get_unverified_user(email: str, db: Session) -> UnverifiedUser:
    return db.query(UnverifiedUser).filter(UnverifiedUser.email == email).first()

def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(id: str, db: Session) -> User:
    return db.query(User).filter(User.id == id).first()

def is_code_valid(email: str, code: str, db: Session) -> bool:
    return db.query(exists().where(
        (UnverifiedUser.email == email) &
        (UnverifiedUser.code == code)
    )).scalar()

def get_wallet(user: User, db: Session) -> Wallet:
    return db.query(Wallet).filter(Wallet.user_id == user.id).first()

def get_transfer_records_of_id(id: int, db: Session):
    return db.query(TransferHistory).filter(
            (TransferHistory.from_user_id == id) |
            (TransferHistory.to_user_id == id)
        ).order_by(TransferHistory.time.desc()).all()