from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    date_of_birth: date
    social_security: str
    address: str
    city: str
    state: str
    post_code: str
    password: str
    verification_code: str

class UserTemp(BaseModel):
    email: EmailStr
    phone_number: str
    social_security: str

class AvailabilityRequest(BaseModel):
    email: Optional[str] = None
    phone_number: Optional[str] = None
    social_security: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str