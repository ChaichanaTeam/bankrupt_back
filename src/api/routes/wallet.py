from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.wallet import Wallet
from src.models.user import User
from src.schemas.user import UserGet
from src.db.dependencies import get_db

router: APIRouter = APIRouter()

def get_current_user_id(email: str, db: Session) -> int:
    return db.query(User).filter(User.email == email).first().id

@router.get("/wallet")
def get_balance(user: UserGet, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.user_id == get_current_user_id(user.email, db)).first()

    if not wallet:
        raise HTTPException(status_code=400, detail="Account isn't exists")

    return {"Balance": wallet.balance}