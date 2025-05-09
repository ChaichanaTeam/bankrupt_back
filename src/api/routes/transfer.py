from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.wallet import TransferRequest
from src.db.dependencies import get_db
from src.api.utils.auth import get_current_user
from src.services.transfer import TransferService

router: APIRouter = APIRouter()

@router.post("/card/transfer")
def transfer_money(transfer: TransferRequest,
                   db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    TransferService.transfer_money_logic(transfer, db, user)

    return {
        f"Transferred {transfer.amount}"
    }

@router.get("/card")
def get_card_info(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    info = TransferService.get_card_info_logic(user, db)

    return info


@router.get("/card/history")
def get_transfer_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    records = TransferService.get_transfer_history_logic(user, db)

    return records