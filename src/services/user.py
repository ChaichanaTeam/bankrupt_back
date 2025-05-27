from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.schemas.user import UserCreate, UserTemp
from src.models.user import User, UnverifiedUser
from src.models.wallet import Wallet
from src.db.queries import is_user_existing, is_code_valid, get_unverified_user
from src.api.utils.auth import create_verification_code
from src.api.utils.mail import send_verification_email
from src.models.cards import Card
from src.db.queries import get_cards, get_user_by_card_number
from src.core.exceptions import user_not_found, forbidden_wallet_action, card_not_found
from src.core.exceptions import user_exists_exception, code_verification_exception, credentials_exception, bad_requset
from src.services.base_user import BaseUserService
from src.core.traceback import traceBack, TrackType
from typing import Any

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(BaseUserService):
    @staticmethod
    def check_availability(payload: dict[str, str], db: Session) -> dict[str, bool]:
        fields_to_check = {
            "email": [User.email, UnverifiedUser.email],
            "phone_number": [User.phone_number, UnverifiedUser.phone_number],
            "social_security": [User.social_security, UnverifiedUser.social_security],
        }

        result = {}
        for field, value in payload.items():
            if field in fields_to_check:
                result[field] = True
                for column in fields_to_check[field]:
                    model_class = column.class_
                    exists = db.query(model_class).filter(column == value).first()
                    if exists:
                        result[field] = False
                        break
        return result

    @staticmethod
    def register(user: UserTemp, db: Session):
        if is_user_existing(user, db):
            raise user_exists_exception

        verification_code = create_verification_code()
        temp_user: UnverifiedUser = UnverifiedUser(
            email=user.email,
            social_security=user.social_security,
            phone_number=user.phone_number,
            code=verification_code
        )
        
        db.add(temp_user)

        try:
            send_verification_email(temp_user.email, verification_code)
        except Exception as e:
            traceBack(f"{e}", type=TrackType.ERROR)
            db.rollback()
            raise bad_requset()

        db.commit()
        db.refresh(temp_user)

    @staticmethod
    def verify_email(user_data: UserCreate, db: Session):
        if not is_code_valid(user_data.email, user_data.verification_code, db):
            raise code_verification_exception

        temp_user = get_unverified_user(user_data.email, db)

        new_user = User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            date_of_birth=user_data.date_of_birth,
            social_security=user_data.social_security,
            address=user_data.address,
            city=user_data.city,
            state=user_data.state,
            post_code=user_data.post_code,
            hashed_password=pwd_context.hash(user_data.password)
        )

        db.add(new_user)
        db.delete(temp_user)
        db.commit()

        db.refresh(new_user)
        
        new_wallet: Wallet = Wallet(
            user_id=new_user.id
        )

        db.add(new_wallet)
        db.commit()
        db.refresh(new_wallet)

    @staticmethod
    def get_user_base_data(user: User, db: Session) -> dict[str, Any]:
        if not user:
            raise credentials_exception()
        
        # wallet: Wallet = get_wallet(user, db)
        card = get_cards(user, db)
        if not card:
            raise user_not_found

        data = {
                "name": user.first_name,
                "surname": user.last_name,
                "balance": card.balance
                }

        return data