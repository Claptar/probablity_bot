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
from app import config
from sqlalchemy import create_engine
from app.database.quieries.utils import session_scope


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
    first_name = Column(String, nullable=True)
    username = Column(String, nullable=False)
    last_trial_id = Column(Integer, ForeignKey("exercises.id"), nullable=True)

    exercise = relationship("Exercise")

    def create(user_data: Dict[str, str]) -> "User":
        """
        Create a new user in the database
        Args:
            user_data (Dict[str, str]): user data
        Returns:
            User: created user
        """
        engine = create_engine(config.DATABASE_URL)
        with session_scope(engine) as session:
            user = User(**user_data)
            session.add(user)
        return user
