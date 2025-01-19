from typing import Dict, Optional
from app.database.models.base import Base
from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.exc import IntegrityError


class User(Base):
    """
    Represents a table with user information

    Attributes:
        id: Unique identifier
        telegram_id: Telegram's user id
        first_name: First name of the user
        username: Username of the user
        last_trial_id: Last exercise id that the user tried
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, nullable=False)
    first_name = Column(String)
    username = Column(String)
    last_trial_id = Column(Integer, ForeignKey("exercises.id"))

    exercise = relationship("Exercise")
