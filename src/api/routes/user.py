from typing import Generator, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import Column
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate
from src.db.session import SessionLocal
from src.models.user import User
from passlib.context import CryptContext

router: APIRouter = APIRouter()

pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db() -> Generator[Any | Session, Any, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    
    return {"email": new_user.email}