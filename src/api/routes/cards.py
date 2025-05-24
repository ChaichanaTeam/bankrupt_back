from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.cards import TransferRequest, CardHistoryRequest
from src.db.dependencies import get_db
from src.api.utils.auth import get_current_user
from src.services.cards import CardsService

router: APIRouter = APIRouter()
@router.post("/create")
def create_card(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        card = CardsService.create_card_logic(user, db)
        return card
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/transfer")
def transfer_money(transfer: TransferRequest,
                   db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    CardsService.transfer_money_logic(transfer, db, user)

    return {
        f"Transferred {transfer.amount}"
    }

@router.get("")
def get_card_info(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    info = CardsService.get_card_info_logic(user, db)

    return info

@router.post("/history")
def get_transfer_history(
    request: CardHistoryRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = CardsService.get_transfer_history_logic(request.card_number, user, db)
    return records