from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.history import BaseHistory

class TransferHistory(BaseHistory):
    __tablename__ = "transfer_history"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer)
    to_user_id = Column(Integer)
    amount = Column(Float)
    time = Column(DateTime, default=datetime.now)
