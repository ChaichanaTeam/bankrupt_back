from sqlalchemy import Column, Boolean, Integer, Float, DateTime, ForeignKey, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.base import Base

class Goals(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    last_payment_date = Column(DateTime)