from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.wallet import Wallet
from src.models.user import User
from src.schemas.token import Token
from src.db.dependencies import get_db
from src.schemas.wallet import TransferRequest
from src.api.utils.auth import get_current_user
from src.models.wallet_history import TransferHistory

router: APIRouter = APIRouter()

def get_user_id_by_email(email: str, db: Session) -> int:
    return db.query(User).filter(User.email == email).first().id

@router.post("/wallet/transfer")
def transfer_money(transfer: TransferRequest,
                   db: Session = Depends(get_db)):
    sender_id = get_user_id_by_email(transfer.from_email, db)
    receiver = get_user_id_by_email(transfer.to_email, db)

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

    history = TransferHistory(
        from_user_id=sender_id,
        to_user_id=receiver,
        amount=transfer.amount
    )
    db.add(history)
    db.commit()
    db.close()

    return {
        "message": f"Transferred {transfer.amount} {transfer.to_email}"
    }

@router.get("/wallet")
def get_balance(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()

    if not wallet:
        raise HTTPException(status_code=400, detail="Account isn't exists")

    return {"Balance": wallet.balance}


@router.get("/wallet/history")
def get_transfer_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = db.query(TransferHistory).filter(
        (TransferHistory.from_user_id == user.id) |
        (TransferHistory.to_user_id == user.id)
    ).order_by(TransferHistory.time.desc()).all()

    result = []
    for h in records:
        from_user = db.query(User).filter(User.id == h.from_user_id).first()
        to_user = db.query(User).filter(User.id == h.to_user_id).first()

        result.append({
            "from_email": from_user.email if from_user else "Unknown",
            "to_email": to_user.email if to_user else "Unknown",
            "amount": h.amount,
            "time": h.time.strftime("%Y-%m-%d %H:%M:%S")
        })

    db.close()
    return {"history": result}