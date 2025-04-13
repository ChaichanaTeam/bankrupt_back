from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.wallet import Wallet
from src.models.user import User
from src.schemas.user import UserGet
from src.db.dependencies import get_db
from src.schemas.wallet import TransferRequest

router: APIRouter = APIRouter()

def get_current_user_id(email: str, db: Session) -> int:
    return db.query(User).filter(User.email == email).first().id

@router.post("/wallet/transfer")
def transfer_money(transfer: TransferRequest,
                   db: Session = Depends(get_db)):
    sender_id = get_current_user_id(transfer.from_email, db)
    receiver = get_current_user_id(transfer.to_email, db)

    if not receiver:
        raise HTTPException(status_code=400, detail="Receiver not Found")

    sender_wallet = db.query(Wallet).filter(Wallet.id == sender_id).first()
    receiver_wallet = db.query(Wallet).filter(Wallet.id == receiver).first()

    if not sender_wallet or receiver_wallet is None:
        raise HTTPException(status_code=400, detail="Sender or Receiver not Found")

    if sender_wallet.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Not enough funds")

    sender_wallet.balance -= transfer.amount
    receiver_wallet.balance += transfer.amount

    db.commit()
    db.refresh(sender_wallet)
    db.refresh(receiver_wallet)

    return {
        "message": f"Transferred {transfer.amount} {transfer.to_email}"
    }



@router.get("/wallet")
def get_balance(user: UserGet, db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.user_id == get_current_user_id(user.email, db)).first()

    if not wallet:
        raise HTTPException(status_code=400, detail="Account isn't exists")

    return {"Balance": wallet.balance}