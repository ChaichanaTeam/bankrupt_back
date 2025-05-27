from sqlalchemy import Column, Boolean, Integer, Float, DateTime, ForeignKey, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from src.db.base import Base
from enum import Enum

class NotificationType(Enum):
    SECURITY = 0
    BILL_DUE = 1
    DEPOSIT = 2

class Notifications(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    notification_type = Column(SQLEnum(NotificationType))
    message = Column(String)
    created_at = Column(DateTime)