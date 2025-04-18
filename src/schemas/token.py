from pydantic import BaseModel

class Token(BaseModel):
    token_type: str = "bearer"
    access_token: str