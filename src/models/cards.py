from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, text, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.db.base import Base

class Card(Base):
    __tablename__ = 'cards'

    id: Column = Column(Integer, primary_key=True)
    cardholder_name: Column = Column(String, nullable=False)
    cardholder_surname: Column = Column(String, nullable=False)
    number: Column = Column(String, nullable=False)
    expiration_date: Column = Column(String, nullable=False)
    cvv: Column = Column(String, nullable=False)
    balance: Column = Column(Float, default=50.0)

    wallet_id: Column = Column(Integer, ForeignKey('wallets.id'), nullable=False)

    wallet = relationship("Wallet", back_populates="cards")
