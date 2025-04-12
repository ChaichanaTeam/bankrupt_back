from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from src.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Column = Column(Integer, primary_key=True, index=True)
    firts_name: Column = Column(String, nullable=False)
    last_name: Column = Column(String, nullable=False)
    email: Column = Column(String, unique=True, nullable=False, index=True)
    phone_number: Column = Column(String, unique=True, nullable=False, index=True)
    date_of_birth: Column = Column(Date, nullable=False)
    social_security: Column = Column(String, unique=True, nullable=False)
    adress: Column = Column(String, nullable=False)
    city: Column = Column(String, nullable=False)
    state: Column = Column(String, nullable=False)
    post_code: Column = Column(String, nullable=False)
    hashed_password: Column = Column(String, nullable=False)

    wallets = relationship("Wallet", back_populates="users")