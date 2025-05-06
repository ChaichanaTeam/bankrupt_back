from pydantic import BaseModel, EmailStr, Field
from src.schemas.token import Token

class TransferRequest(BaseModel):
    to_card_number: str
    amount: float = Field(..., gt=0, description="Amount must be positive")