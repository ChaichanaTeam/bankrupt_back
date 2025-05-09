from sqlalchemy.orm import Session
from src.models.wallet import Wallet
from src.models.user import User
from src.models.cards import Card
from src.models.wallet_history import TransferHistory
from src.core.exceptions import user_not_found, forbidden_wallet_action, card_not_found
from src.db.queries import get_card, get_user_by_card_number, get_card_transfer_history_records


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
            from_user_card_number = sender_card.number,
            from_user=f"{sender_card.cardholder_name} {sender_card.cardholder_surname}",
            to_user_card_number=receiver_card.number,
            to_user=f"{receiver_card.cardholder_name} {receiver_card.cardholder_surname}",
            amount=transfer.amount
        )

        db.add(history_record)
        db.commit()
        db.refresh(sender_card)
        db.refresh(receiver_card)

        return history_record

    @staticmethod
    def get_card_info_logic(user: User, db: Session) -> float:
        cards = get_card(user, db)
        if not cards:
            raise user_not_found

        return [
            {
                "number": card.number,
                "cardholder_name": card.cardholder_name,
                "cardholder_surname": card.cardholder_surname,
                "expiration_date": card.expiration_date,
                "cvv": card.cvv,
                "balance": card.balance
            }
            for card in cards
        ]

    @staticmethod
    def get_transfer_history_logic(user: User, db: Session) -> dict[str, list]:
        card = get_card(user, db)
        if not card:
            return {"history": []}

        records = get_card_transfer_history_records(card, db)

        result = []
        for record in records:
            direction = (
                "out" if record.from_user_card_number == card.number else "in"
            )

            result.append({
                "direction": direction,
                "from": record.from_user,
                "to": record.to_user,
                "amount": record.amount,
                "time": record.time.isoformat()
            })

        return {"history": result}
