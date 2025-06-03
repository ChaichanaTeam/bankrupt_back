from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.savings import Saving_Account_creation, Saving_Account_out, Saving_Account_TopUp, Saving_Account_Delete
from src.db.dependencies import get_db
from src.api.utils.auth import get_current_user_cookie
from src.services.savings import SavingsService
from typing import List

router: APIRouter = APIRouter()
@router.post("/create")
def create_saving_account(data: Saving_Account_creation, db: Session = Depends(get_db), user: User = Depends(get_current_user_cookie)):
    try:
        saving_account = SavingsService.create_saving_account(user, data, db)
        return saving_account
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[Saving_Account_out])
def get_saving_accounts(user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    try:
        return SavingsService.get_user_saving_accounts(user, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/topUp")
def topUp_saving_account(data: Saving_Account_TopUp, user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):

    try:
        return SavingsService.add_funds(data, user, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return{
        f"Added {amount}"
    }

@router.post("/decrease")
def decrease_saving_account(data: Saving_Account_TopUp, user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):

    try:
        return SavingsService.take_funds(data, user, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return{
        f"Taken {amount}"
    }


@router.post("/delete")
def delete_saving_account(data: Saving_Account_Delete, user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    try:
        return SavingsService.delete_saving_account_logic(user, data.saving_account_id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))