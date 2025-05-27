from sqlalchemy import exists
from sqlalchemy.orm import Session
from src.core.exceptions import user_not_found, forbidden_wallet_action, bad_requset
from src.db.queries import get_wallet, get_cards, get_card_by_id, get_saving_accounts, get_saving_account_by_id
from src.models.user import User
from src.models.savings import Saving_account
from src.schemas.savings import Saving_Account_creation, Saving_Account_out
from typing import List


class SavingsService:
    @staticmethod
    def create_saving_account(user: User, data: Saving_Account_creation, db: Session) -> dict:
        wallet = get_wallet(user, db)
        if not wallet:
            raise user_not_found

        new_saving_account: Saving_account = Saving_account(
            wallet_id = wallet.id,
            name = data.name,
            goal = data.goal
        )

        db.add(new_saving_account)
        db.commit()
        db.refresh(new_saving_account)

        return {
            "id": new_saving_account.id,
            "name": new_saving_account.name,
            "goal": new_saving_account.goal,
            "balance": new_saving_account.balance
        }

    @staticmethod
    def get_user_saving_accounts(user: User, db: Session) -> List[Saving_Account_out]:
        wallet = get_wallet(user, db)
        if not wallet:
            raise user_not_found

        accounts = db.query(Saving_account).filter(Saving_account.wallet_id == wallet.id).all()

        return [
            {
                "id": account.id,
                "name": account.name,
                "balance": account.balance,
                "goal": account.goal,
                "remain": (account.goal - account.balance)
            }
            for account in accounts
        ]



    @staticmethod
    def add_funds(data, user: User, db: Session) -> dict:

        wallet = get_wallet(user, db)
        saving_account = get_saving_account_by_id(user, data.saving_account_id, db)
        card = get_card_by_id(user, data.card_id, db)

        if not wallet or not saving_account or not card:
            raise user_not_found

        if card.balance < data.amount:
            raise forbidden_wallet_action("Not enough funds")

        card.balance -= data.amount
        saving_account.balance += data.amount

        db.commit()
        db.refresh(saving_account)
        db.refresh(card)

    @staticmethod
    def take_funds(data, user: User, db: Session) -> dict:

        wallet = get_wallet(user, db)
        saving_account = get_saving_account_by_id(user, data.saving_account_id, db)
        card = get_card_by_id(user, data.card_id, db)

        if not wallet or not saving_account or not card:
            raise user_not_found

        if saving_account.balance < data.amount:
            raise forbidden_wallet_action("Not enough funds")

        card.balance += data.amount
        saving_account.balance -= data.amount

        db.commit()
        db.refresh(saving_account)
        db.refresh(card)

