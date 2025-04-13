from datetime import date

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    date_of_birth: date
    social_security: str
    adress: str
    city: str
    state: str
    post_code: str
    password: str

class UserGet(BaseModel):
    email: EmailStr

class UserLogin(BaseModel):
    email: str
    password: str