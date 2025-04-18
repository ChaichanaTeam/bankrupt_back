from sqlalchemy.orm import Session
from src.models.wallet import Wallet
from src.models.user import User
from src.models.wallet_history import TransferHistory
from src.core.exceptions import user_not_found, forbidden_wallet_action
from src.db.queries import get_user_by_email, get_wallet, get_user_by_id, get_transfer_records_of_id

class WalletService:
    @staticmethod
    def transfer_money_logic(transfer, db: Session, user: User):
        receiver = get_user_by_email(transfer.to_email, db)
        if not receiver:
            raise user_not_found

        sender_wallet: Wallet = get_wallet(user, db)
        receiver_wallet: Wallet = get_wallet(receiver, db)

        if not sender_wallet or not receiver_wallet:
            raise user_not_found

        if sender_wallet.balance < transfer.amount:
            raise forbidden_wallet_action("Not enough funds")

        sender_wallet.balance -= transfer.amount
        receiver_wallet.balance += transfer.amount

        history_record = TransferHistory(
            from_user_id=user.id,
            to_user_id=receiver.id,
            amount=transfer.amount
        )

        db.add(history_record)
        db.commit()
        db.refresh(sender_wallet)
        db.refresh(receiver_wallet)

        return history_record

    @staticmethod
    def get_balance_logic(user: User, db: Session) -> float:
        wallet = get_wallet(user, db)
        if not wallet:
            raise user_not_found
        
        return wallet.balance

    @staticmethod
    def get_transfer_history_logic(user: User, db: Session) -> dict[str, list]:
        records = get_transfer_records_of_id

        result = []
        for record in records:
            from_user = get_user_by_id(record.from_user_id)
            to_user = get_user_by_id(record.to_user_id)

            result.append({
                "from_email": from_user.email if from_user else "Unknown",
                "to_email": to_user.email if to_user else "Unknown",
                "amount": record.amount,
                "time": record.time.strftime("%Y-%m-%d %H:%M:%S")
            })

        return { "history": result }
