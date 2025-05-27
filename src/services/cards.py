import random
from datetime import datetime, timedelta
from src.models.cards import Card
from sqlalchemy import exists
from sqlalchemy.orm import Session
# from src.models.wallet import Wallet
from src.models.user import User
from src.models.wallet_history import TransferHistory
from src.core.exceptions import user_not_found, forbidden_wallet_action
from src.db.queries import get_user_by_email, get_wallet, get_user_by_id, get_transfer_records_of_id

def generate_card_number(db: Session):
    while True:
        number = ''.join(str(random.randint(0, 9)) for _ in range(16))
        if not db.query(exists().where(Card.number == number)).scalar():
            return number
    
def generate_cvv():
    return ''.join(str(random.randint(0, 9)) for _ in range(3))

def generate_expiration_date():
    future_date = datetime.now() + timedelta(days=365 * 5)
    return future_date.strftime("%m/%y")

class CardsService:
    @staticmethod
    def create_card_logic(user: User, db: Session) -> dict:
        wallet = get_wallet(user, db)
        if not wallet:
            raise user_not_found

        card_number = generate_card_number(db)
        card_cvv = generate_cvv()
        card_expiry = generate_expiration_date()

        card = Card(
            wallet_id = wallet.id,
            cardholder_name=user.first_name,
            cardholder_surname=user.last_name,
            number = card_number,
            expiration_date = card_expiry,
            cvv = card_cvv
        )

        db.add(card)
        db.commit()
        db.refresh(card)

        return card.json()