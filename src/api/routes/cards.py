from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.wallet import TransferRequest
from src.db.dependencies import get_db
from src.api.utils.auth import get_current_user
from src.db.queries import get_cards
# from src.services.wallet import WalletService
from src.services.cards import CardsService

router: APIRouter = APIRouter()

@router.get("/cards/{four_digits}")
def get_card(four_digits: str, 
             user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cards = get_cards(user, db)
    card = next((_card for _card in cards if _card.number[-4:] == four_digits), None)

    return card.json()

@router.post("/cards/create")
def create_card(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        card = CardsService.create_card_logic(user, db)
        return card
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))