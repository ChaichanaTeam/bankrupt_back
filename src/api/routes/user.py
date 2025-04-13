from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserLogin
from src.schemas.token import Token
from src.models.user import User
from src.models.wallet import Wallet
from passlib.context import CryptContext
from src.db.dependencies import get_db
from src.api.utils.auth import create_access_token

router: APIRouter = APIRouter()

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_existed_user(user: UserCreate, db: Session) -> User:
    return db.query(User).filter(User.email == user.email).first() or \
    db.query(User).filter(User.social_security == user.social_security).first() or \
    db.query(User).filter(User.phone_number == user.phone_number).first()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing: User = get_existed_user(user, db)
    if existing:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_pw: str = pwd_context.hash(user.password)
    new_user: User = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        date_of_birth=user.date_of_birth,
        social_security=user.social_security,
        adress=user.adress,
        city=user.city,
        state=user.state,
        post_code=user.post_code,
        hashed_password=hashed_pw
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

    return {"email": new_user.email}

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not pwd_context.verify(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}