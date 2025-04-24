from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.wallet import TransferRequest
from src.db.dependencies import get_db
from src.api.utils.auth import get_current_user
from src.services.wallet import WalletService
from src.services.cards import CardsService

router: APIRouter = APIRouter()
@router.post("/cards/create")
def create_card(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        card = CardsService.create_card_logic(user, db)
        return card
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))