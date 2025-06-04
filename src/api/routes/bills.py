from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.models.user import User
from src.schemas.bills import BillCreate, BillOut, BillPay
from src.db.dependencies import get_db
from src.api.utils.auth import get_current_user_cookie
from src.services.bills import BillsService

router: APIRouter = APIRouter()

@router.post("/create")
def create_bill(data: BillCreate, user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    try:
        return BillsService.create_bill(user, data, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[BillOut])
def get_user_bills(user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    try:
        return BillsService.get_user_bills(user, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/pay")
def pay_bill(data: BillPay, user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    try:
        return BillsService.pay_bill(user, data.bill_id, data.card_number, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))