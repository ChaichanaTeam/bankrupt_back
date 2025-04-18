from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Any
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.models.user import User
from src.core.config import settings
from src.core.exceptions import credentials_exception
from src.db.dependencies import get_db
from src.db.queries import get_user_by_email
import random, string

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_verification_code() -> str:
    nums = random.choices(string.digits, k=4)
    letters = random.choices(string.ascii_uppercase, k=4)
    
    code = letters + nums
    random.shuffle(code)
    return ''.join(code)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload: dict[str, Any] = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email(email, db)
    if user is None:
        raise credentials_exception
    
    return user