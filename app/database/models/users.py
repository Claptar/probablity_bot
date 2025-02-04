"Contains the User class that represents a user, stored in the database"
import logging
from typing import Dict, Type, List, Any
from sqlalchemy import Integer, String, Column, ForeignKey, desc
from sqlalchemy.orm import relationship, Session
from app.database.models.base import Base
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

        logging.info("Creating a new user with data: %s", user_data)

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
                logging.warning(
                    "User %s exists in the database. Updating the user data", user_data
                )
                user.first_name = user_data.get("first_name", None)
                user.username = user_data.get("username", None)
            else:
                user = cls(**user_data)

            # add the user to the table
            session.add(user)
        return user

    @classmethod
    def user_by_telegram_id(
        cls: Type["User"], telegram_id: int, session: Session
    ) -> "User":
        """
        Get the user by telegram id
        Args:
            telegram_id (int): Telegram's user id
            session (Session): SQLAlchemy session
        Returns:
            User: User object
        """
        user = session.query(cls).filter_by(telegram_id=telegram_id).one_or_none()
        if user:
            return user
        else:
            raise ValueError(
                f"User with telegram id {telegram_id} not found in the database"
            )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the User object to a dictionary
        Returns:
            Dict[str, Any]: Dictionary representation of the User object
        """
        return {
            "id": self.id,
            "username": self.username,
            "score": self.score,
            "telegram_id": self.telegram_id,
        }

    @classmethod
    def get_solution(cls, telegram_id: int) -> str:
        """
        Get the solution of the last exercise that the user tried
        Args:
            telegram_id (int): Telegram's user id
        Returns:
            str: Solution text of the last exercise
        """
        with session_scope() as session:
            user = cls.user_by_telegram_id(telegram_id, session)
            if user.last_trial_id is None:
                raise ValueError("User has not tried any exercise yet")
            return user.exercise.contents

    @classmethod
    def update_exercise(cls, telegram_id: int, exercise_id: int) -> None:
        """
        Update the last exercise that the user tried
        Args:
            telegram_id (int): Telegram's user id
            exercise_id (int): Exercise id
        """
        with session_scope() as session:
            user = cls.user_by_telegram_id(telegram_id, session)
            user.last_trial_id = exercise_id

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
            user = cls.user_by_telegram_id(telegram_id, session)
            return user.score

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
