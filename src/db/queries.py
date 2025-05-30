from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import exists, select
from src.schemas.user import UserCreate, UserLogin
from src.schemas.token import Token
from src.models.wallet import Wallet
from src.models.wallet_history import TransferHistory
from src.models.cards import Card
from src.models.user import User, UnverifiedUser
from src.models.savings import Saving_account
from src.models.bills import Bills
from typing import Optional

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

def get_expired_users(db: Session, threshold: datetime = datetime.now(timezone.utc)) -> list[UnverifiedUser]:
    return db.query(UnverifiedUser).filter(UnverifiedUser.created_at < threshold).all()

def get_unverified_user(email: str, db: Session) -> UnverifiedUser:
    return db.query(UnverifiedUser).filter(UnverifiedUser.email == email).first()

def get_user_by_email(email: str, db: Session) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_card_number(db: Session, card_number: str) -> Optional[User]:
    return(
        db.query(User)
        .join(Wallet, User.id == Wallet.user_id)
        .join(Card, Wallet.id == Card.wallet_id)
        .filter(Card.number == card_number).first()
    )

def get_user_by_id(id: int, db: Session) -> User:
    return db.query(User).filter(User.id == id).first()

def is_code_valid(email: str, code: str, db: Session) -> bool:
    return db.query(exists().where(
        (UnverifiedUser.email == email) &
        (UnverifiedUser.code == code)
    )).scalar()

def get_wallet(user: User, db: Session) -> Wallet:
    return db.query(Wallet).filter(Wallet.user_id == user.id).first()

def get_cards(user: User, db: Session) -> list[Card]:
    return (
        db.query(Card)
        .join(Wallet, Card.wallet_id == Wallet.id)
        .filter(Wallet.user_id == user.id).all()
    )

def get_card_by_id(user: User, card_id: int, db: Session) -> Optional[Card]:
    return (
        db.query(Card)
        .join(Wallet, Card.wallet_id == Wallet.id)
        .filter(
            Wallet.user_id == user.id,
            Card.id == card_id
        )
        .first()
    )


def get_card_by_number(user: User, card_number: str, db: Session) -> Optional[Card]:
    return(
        db.query(Card)
        .join(Wallet, Card.wallet_id == Wallet.id)
        .filter(
            Wallet.user_id == user.id,
            Card.number == card_number
        )
        .first()
    )


def get_transfer_records_of_id(id: int, db: Session):
    return db.query(TransferHistory).filter(
            (TransferHistory.from_user_id == id) |
            (TransferHistory.to_user_id == id)
        ).order_by(TransferHistory.time.desc()).all()

def get_card_transfer_history_records(card: Card, db: Session) -> list[TransferHistory]:
    return (
        db.query(TransferHistory).filter(
            (TransferHistory.from_user_card_number == card.number) |
            (TransferHistory.to_user_card_number == card.number)
        )
        .order_by(TransferHistory.time.desc())
        .all()
    )

def get_saving_accounts(user: User, db: Session):
    return(
        db.query(Saving_account).join(Wallet, Saving_account.wallet_id == Wallet.id)
        .filter(Wallet.user_id == user.id).all()
    )

def get_saving_account_by_id(user: User, account_id: int, db: Session) -> Optional[Saving_account]:
    return (
        db.query(Saving_account)
        .join(Wallet, Saving_account.wallet_id == Wallet.id)
        .filter(
            Wallet.user_id == user.id,
            Saving_account.id == account_id
        )
        .first()
    )

def get_bill_by_id(user, bill_id: int, db: Session):
    return (
        db.query(Bills)
        .filter(Bills.id == bill_id, Bills.wallet_id == get_wallet(user, db).id)
        .first()
    )

def is_superuser(id: int, db: Session) -> bool:
    return db.query(exists().where(
        (User.id == id) &
        (User.is_superuser == True)
    )).scalar()

def get_all_users(db: Session) -> list[User]:
    return db.execute(select(User)).scalars().all()