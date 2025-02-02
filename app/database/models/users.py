from typing import Dict, Type, List
from app.database.models.base import Base
from sqlalchemy import Integer, String, Column, ForeignKey, desc
from sqlalchemy.orm import relationship, joinedload
from app.database.quieries.utils import session_scope
import logging

logger = logging.getLogger(__name__)


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
    username = Column(String, nullable=True)
    score = Column(Integer, default=0)
    last_trial_id = Column(Integer, ForeignKey("exercises.id"), nullable=True)

    exercise = relationship("Exercise")
    solved_exercises = relationship(
        "SolvedExercise", back_populates="user", uselist=True
    )

    @classmethod
    def create(cls: Type["User"], **user_data: Dict[str, str]) -> "User":
        """
        Create a new user in the database
        Args:
            user_data (Dict[str, str]): user data
        Returns:
            User: created user
        """

        logger.info(f"Creating a new user with data: {user_data}")

        # check if there is telegram_id in the user_data
        if "telegram_id" not in user_data.keys():
            raise ValueError("Telegram id is required to create a user")

        with session_scope() as session:
            # check if the user already exists in the database
            user = (
                session.query(cls)
                .filter_by(telegram_id=user_data["telegram_id"])
                .one_or_none()
            )
            if user:
                logger.warning(
                    f"User {user_data} exists in the database. Updating the user data"
                )
                user.first_name = user_data.get("first_name", None)
                user.username = user_data.get("username", None)
            else:
                user = cls(**user_data)

            # add the user to the table
            session.add(user)
        return user

    @classmethod
    def update_exercise(cls, telegram_id: int, exercise_id: int) -> None:
        """
        Update the last exercise that the user tried
        Args:
            telegram_id (int): Telegram's user id
            exercise_id (int): Exercise id
        """
        with session_scope() as session:
            user = session.query(cls).filter_by(telegram_id=telegram_id).one_or_none()
            if user:
                user.last_trial_id = exercise_id
            else:
                raise ValueError(
                    f"User with telegram id {telegram_id} not found in the database"
                )

    @classmethod
    def user_score(cls, telegram_id: int) -> int:
        """
        Get the user's score
        Args:
            telegram_id (int): Telegram's user id
        Returns:
            int: User's score
        """
        with session_scope() as session:
            user = (
                session.query(cls)
                .options(joinedload(cls.solved_exercises))
                .filter_by(telegram_id=telegram_id)
                .one_or_none()
            )
            if user:
                return user.score
            else:
                raise ValueError(
                    f"User with telegram id {telegram_id} not found in the database"
                )

    @staticmethod
    def _userlist_to_leaderboard(userlist: List["User"]) -> str:
        """
        Convert a list of users to a leaderboard string
        Args:
            userlist (List[User]): List of users
        Returns:
            str: Leaderboard string
        """
        emoji_list = ["🥇", "🥈", "🥉"] + ["🔹"] * 7
        leaderboard = [
            f"{emoji_list[i]} @{user.username}: *{user.score}{'s' if user.score > 1 else ''} points*"
            for i, user in enumerate(userlist)
        ]
        header = "💥*Strongest challengers*💥\n\n"
        leaderboard = header + "\n".join(leaderboard)
        return leaderboard

    @classmethod
    def get_top_users(cls, limit: int = 7):
        """
        Get the top users with the highest scores
        Args:
            limit (int): Number of top users to retrieve
        Returns:
            List[User]: List of top users
        """
        with session_scope() as session:
            top_users = session.query(cls).order_by(desc(cls.score)).limit(limit).all()
            return cls._userlist_to_leaderboard(top_users)
