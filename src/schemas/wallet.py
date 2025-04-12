from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    balance: float
    user_id: int