from fastapi import APIRouter, Depends
from sqlalchemy import Column
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserLogin, UserTemp, AvailabilityRequest
from src.schemas.token import Token
from src.models.user import User, UserTemp as UnverifiedUser
from src.models.wallet import Wallet
from passlib.context import CryptContext
from src.db.dependencies import get_db
from src.api.utils.auth import create_access_token, create_verification_code
from src.api.utils.mail import send_verification_email
from src.core.exceptions import user_exists_exception, code_verification_exception, credentials_exception
from src.db.queries import is_user_existing, is_code_valid, get_unverified_user, get_user

router: APIRouter = APIRouter()

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

FIELDS_TO_CHECK = {
    "email": [User.email, UnverifiedUser.email],
    "phone_number": [User.phone_number, UnverifiedUser.phone_number],
    "social_security": [User.social_security, UnverifiedUser.social_security],
}

@router.get("/check-availability")
def check_availability(payload: AvailabilityRequest, db: Session = Depends(get_db())):
    result: dict[str, bool] = {}
    values: dict[str, str] = payload.model_dump(exclude_none=True)

    for field, value in values.items():
        if field in FIELDS_TO_CHECK:
            result[field] = True
            for column in FIELDS_TO_CHECK[field]:
                model_class = column.class_
                exists = db.query(model_class).filter(column == value).first()
                
                if exists:
                    result[field] = False
                    break

    return result


@router.post("/register")
def register_user(user: UserTemp, db: Session = Depends(get_db)):
    existing: User = is_user_existing(user.email, db)
    if existing:
        raise user_exists_exception

    verification_code: str = create_verification_code()

    temp_user: UnverifiedUser = UnverifiedUser(
            email=user.email,
            social_security=user.social_security,
            phone_number=user.phone_number,
            code=verification_code
        )

    db.add(temp_user)
    db.commit()
    db.refresh(temp_user)

    send_verification_email(temp_user.email, verification_code)

    return {"message": "Mail has been send"}

@router.post("/verify-email")
def verify_email(user: UserCreate, db: Session = Depends(get_db)):
    if not is_code_valid(user.email, user.verification_code, db):
        raise code_verification_exception

    temp_user: UnverifiedUser = get_unverified_user(user.email, db)

    db.delete(temp_user)
    db.commit()

    new_user: User = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        date_of_birth=user.date_of_birth,
        social_security=user.social_security,
        address=user.address,
        city=user.city,
        state=user.state,
        post_code=user.post_code,
        hashed_password=pwd_context.hash(user.password)#,
        #created_at= Не знаю что писать
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    new_wallet: Wallet = Wallet(
        user_id=new_user.id
    )

    db.add(new_wallet)
    db.commit()
    db.refresh(new_wallet)

    return {"message": "Verification passed. Wallet attached"}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = get_user(user_data.email, db)

    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise credentials_exception

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "Bearer"}

## TODO login 2FA