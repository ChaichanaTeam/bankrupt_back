from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.schemas.user import UserCreate, UserLogin, UserTemp, AvailabilityRequest, UserPasswordReset
from src.db.dependencies import get_db
from src.services.user import UserService
from src.models.user import User
from src.api.utils.auth import get_current_user_cookie

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
    user_data = UserLogin(email=user.email, password=user.password)
    return UserService.login(user_data, db)

@router.post("/2fa/request")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return UserService.twofa_request(user_data, db)

@router.post("/2fa/confirm")
def twofa_confirm(user_data: UserLogin, db: Session = Depends(get_db)):
    return UserService.twofa_confirm(user_data, db)

@router.get("/me")
def get_user_base_data(user: User = Depends(get_current_user_cookie), db: Session = Depends(get_db)):
    return UserService.get_user_base_data(user, db)

@router.post("/reset")
def reset_password_request(user_reset: UserTemp, db: Session = Depends(get_db)):
    return UserService.reset_password_request(user_reset, db)

@router.patch("/reset")
def reset_password_confirm(password_form: UserPasswordReset, db: Session = Depends(get_db)):
    return UserService.reset_password_confirm(password_form, db)

@router.get("/logout")
def logout():
    return UserService.logout()