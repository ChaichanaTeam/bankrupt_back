from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base

class Wallet(Base):
    __tablename__ = 'wallets'

    id: Column = Column(Integer, primary_key=True, index=True)
    balance: Column = Column(Float, default = 0.0)

    user_id = Column(Integer, ForeignKey('users.id'))

    users = relationship('User', back_populates='wallets')