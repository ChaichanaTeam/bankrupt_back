from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.models.user import User
from src.schemas.cards import TransferRequest, CardHistoryRequest, CardDelete
from src.db.dependencies import get_db
from src.api.utils.auth import get_current_user_cookie
from src.db.queries import get_cards
from src.services.cards import CardsService

router: APIRouter = APIRouter()

@router.get("/{four_digits}")
def get_card(four_digits: str, 
             user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    cards = get_cards(user, db)
    card = next((_card for _card in cards if _card.number[-4:] == four_digits), None)

    return card.json()

@router.post("/create")
def create_card(user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    try:
        card = CardsService.create_card_logic(user, db)
        return card
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete")
def delete_card(card_delete: CardDelete, user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    try:
        result = CardsService.delete_card_logic(user, card_delete.card_number, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/transfer")
def transfer_money(transfer: TransferRequest,
                   db: Session = Depends(get_db),
                   user: User = Depends(get_current_user_cookie)):
    CardsService.transfer_money_logic(transfer, user, db)

    return {
        f"Transferred {transfer.amount}"
    }

@router.get("")
def get_card_info(user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    return CardsService.get_card_info_logic(user, db)

@router.post("/history")
def get_transfer_history(
    request: CardHistoryRequest,
    user: User = Depends(get_current_user_cookie),
    db: Session = Depends(get_db)
):
    records = CardsService.get_transfer_history_logic(request.card_number, user, db)
    return records