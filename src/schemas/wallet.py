from pydantic import BaseModel, EmailStr, Field

class WalletGet(BaseModel):
    balance: float
    user_id: int

class TransferRequest(BaseModel):
    from_email: EmailStr
    to_email: EmailStr
    amount: float = Field(..., gt=0, description="Amount must be positive")