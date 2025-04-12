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


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_pw = pwd_context.hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"email": new_user.email}