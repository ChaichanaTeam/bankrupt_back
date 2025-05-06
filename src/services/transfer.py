from sqlalchemy.orm import Session
from src.models.wallet import Wallet
from src.models.user import User
from src.models.cards import Card
from src.models.wallet_history import TransferHistory
from src.core.exceptions import user_not_found, forbidden_wallet_action, card_not_found
from src.db.queries import get_card, get_user_by_card_number


class TransferService:
    @staticmethod
    def transfer_money_logic(transfer, db: Session, user: User):
        receiver = get_user_by_card_number(db, transfer.to_card_number)
        if not receiver:
            raise user_not_found

        sender_card: Card = get_card(user, db)
        receiver_card: Card = get_card(receiver, db)

        if not sender_card or not receiver_card:
            raise card_not_found

        if sender_card.balance < transfer.amount:
            raise forbidden_wallet_action("Not enough funds")

        sender_card.balance -= transfer.amount
        receiver_card.balance += transfer.amount

        history_record = TransferHistory(
            from_user_id=user.id,
            to_user_id=receiver.id,
            amount=transfer.amount
        )

        db.add(history_record)
        db.commit()
        db.refresh(sender_card)
        db.refresh(receiver_card)

        return history_record

    @staticmethod
    def get_balance_logic(user: User, db: Session) -> float:
        card = get_card(user, db)
        if not card:
            raise user_not_found

        return card.balance

    # @staticmethod
    # def get_transfer_history_logic(user: User, db: Session) -> dict[str, list]:
    #     records = get_transfer_records_of_id
    #
    #     result = []
    #     for record in records:
    #         from_user = get_user_by_id(record.from_user_id)
    #         to_user = get_user_by_id(record.to_user_id)
    #
    #         result.append({
    #             "From": from_user.email if from_user else "Unknown",
    #             "To": to_user.email if to_user else "Unknown",
    #             "amount": record.amount,
    #             "time": record.time.strftime("%Y-%m-%d %H:%M:%S")
    #         })
    #
    #     return {"history": result}
