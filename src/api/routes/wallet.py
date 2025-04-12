from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.models.wallet import Wallet
from src.models.user import User

router: APIRouter = APIRouter()

def get_current_user_id(email: str, db: Session) -> int:
    return db.query(User).filter(User.email == email).first().id

@router.get("/wallet", response_model=Wallet)
def get_balance(user_id: int, db: Session) -> int:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()

    if wallet:
        return wallet.balance
    return None

if __name__ == "__main__":
    db_gen = get_db()
    db = next(db_gen)

    balance = get_balance(get_current_user_id("<EMAIL>", get_db()), get_db())

    print(balance)

    db_gen.close()