from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.base import Base

class TransferHistory(Base):
    __tablename__ = "transfer_history"

    id = Column(Integer, primary_key=True, index=True)
    from_user_card_number = Column(String)
    from_user = Column(String)
    to_user_card_number = Column(String)
    to_user = Column(String)
    amount = Column(Float)
    time = Column(DateTime, default=datetime.now)
