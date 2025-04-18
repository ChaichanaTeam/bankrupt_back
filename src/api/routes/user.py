from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserLogin, UserTemp, AvailabilityRequest
from src.schemas.token import Token
from src.db.dependencies import get_db
from src.services.user import UserService

router: APIRouter = APIRouter()

@router.get("/check-availability")
def check_availability(payload: AvailabilityRequest, db: Session = Depends(get_db)):
    return UserService.check_availability(payload, db)

@router.post("/register")
def register_user(user: UserTemp, db: Session = Depends(get_db)):
    UserService.register(user, db)
    return {"message": "Mail has been send"}

@router.post("/verify-email")
def verify_email(user: UserCreate, db: Session = Depends(get_db)):
    UserService.verify_email(user, db)
    return {"message": "Verification passed. Wallet attached"}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    token = UserService.login(user_data, db)
    return { "token_type": "Bearer", "access_token": token }

## TODO login 2FA

## Password reset