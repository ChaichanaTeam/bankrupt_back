from pydantic import BaseModel, EmailStr

class WalletGet(BaseModel):
    balance: float
    user_id: int