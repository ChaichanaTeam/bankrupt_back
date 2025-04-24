from pydantic import BaseModel, constr

class CardCreate(BaseModel):
    cardholder_name: str
    cardholder_surname: str
    number: constr(min_length=13, max_length=19)
    expiration_date: str
    cvv: constr(min_length=3, max_length=4)