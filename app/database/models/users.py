"Contains the User class that represents a user, stored in the database"
import logging
from string import Template
from typing import Dict, Type, List, Any
from sqlalchemy import Integer, String, Column, ForeignKey, Boolean, desc, func
from sqlalchemy.orm import relationship, Session
from sqlalchemy.exc import NoResultFound
from app.database.models.base import Base


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
    select_sections = Column(Boolean, default=False)
    select_paragraphs = Column(Boolean, default=False)

    exercise = relationship("Exercise")
    solved_exercises = relationship(
        "SolvedExercise", back_populates="user", uselist=True
    )
    selected_sections = relationship(
        "SelectedSection", back_populates="user", uselist=True
    )
    selected_paragraphs = relationship(
        "SelectedParagraph", back_populates="user", uselist=True
    )

    def __repr__(self) -> str:
        return f"User(telegram_id={self.telegram_id}, first_name={self.first_name}, username={self.username})"

    def __str__(self) -> str:
        return f"User {self.username} with telegram id {self.telegram_id}"

    @classmethod
    def user_by_telegram_id(
        cls: Type["User"], telegram_id: str, session: Session
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
        if not user:
            logging.error(
                "User with telegram_id=%s not found in the database", telegram_id
            )
            raise NoResultFound(
                f"User with telegram id {telegram_id} not found in the database"
            )
        return user

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the User object to a dictionary
        Returns:
            Dict[str, Any]: Dictionary representation of the User object
        """
        return {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "score": self.score,
            "telegram_id": self.telegram_id,
        }

    @staticmethod
    def get_rank_emoji(rank: int) -> str:
        """
        Get the emoji for the user's rank
        Args:
            rank (int): User's rank
        Returns:
            str: Emoji for the user's rank
        """
        top3_emojis = ["🥇", "🥈", "🥉"]
        outer_emoji = "🔹"
        if rank <= 3:
            return top3_emojis[rank - 1]
        return outer_emoji

    @staticmethod
    def get_user_name(user: Dict[str, Any]) -> str:
        """
        Get the user's name
        Args:
            user (Dict[str, Any]): User dictionary
        Returns:
            str: User's name
        """
        if user["username"]:
            return "@" + user["username"]
        elif user["first_name"]:
            return user["first_name"]
        elif user["telegram_id"]:
            return "Challenger" + user["telegram_id"]
        return "Unknown challenger"

    @classmethod
    def user_to_leaderboard(cls, user: Dict[str, Any]) -> str:
        """
        Convert a user to a leaderboard string
        Args:
            user (Dict[str, Any]): User dictionary
        Returns:
            str: Leaderboard string
        """
        leaderboard_template = Template(
            "$rank_emoji $user_name: *$score point${plural_s}*"
        )
        return leaderboard_template.substitute(
            rank_emoji=cls.get_rank_emoji(user["rank"]),
            user_name=cls.get_user_name(user),
            score=user["score"],
            plural_s="s" if user["score"] > 1 else "",
        )

    @classmethod
    def _userlist_to_leaderboard(
        cls, userlist: List["User"], user: Dict[str, Any] = None
    ) -> str:
        """
        Convert a list of users to a leaderboard string
        Args:
            userlist (List[User]): List of users
            user (Dict[str, Any], optional): User dictionary
        Returns:
            str: Leaderboard string
        """
        # create the leaderboard
        leaderboard = [cls.user_to_leaderboard(user) for user in userlist]
        header = "💥*Strongest challengers*💥\n\n"
        leaderboard = header + "\n".join(leaderboard)
        if user in userlist:
            leaderboard += "\n....\n" + cls.user_to_leaderboard(user)
        return leaderboard

    @classmethod
    def get_user_ranking(cls, session: Session) -> List[Dict[str, Any]]:
        """
        Get the user ranking
        Args:
            session (Session): SQLAlchemy session
        Returns:
            List[Dict[str, Any]]: List of users with ranks
        """
        ranked_query = session.query(
            cls,
            func.rank().over(order_by=desc(cls.score)).label("rank"),
        ).all()
        if not ranked_query:
            return NoResultFound("No users found in the database")
        return [{"rank": rank, **user.to_dict()} for user, rank in ranked_query]

    @staticmethod
    def user_ranking(telegram_id: int, user_list: List["User"]) -> str:
        """
        Get the user ranking
        Args:
            telegram_id (int): Telegram's user id
            user_list (List[User]): List of users
        Returns:
            str: User's rank
        """
        for user in user_list:
            if user["telegram_id"] == telegram_id:
                return user.rank
        return NoResultFound(
            "User with telegram_id=%s not found in the ranking", telegram_id
        )

    @classmethod
    def user_leaderboard(
        cls, telegram_id: str, session: Session, limit: int = 5
    ) -> str:
        """
        Get the user leaderboard
        Args:
            telegram_id (str): Telegram's user id
            session (Session): SQLAlchemy session
        Returns:
            str: Leaderboard string
        """
        user_list = cls.get_user_ranking(session)
        user_rank = cls.user_ranking(telegram_id, user_list)
        return cls._userlist_to_leaderboard(user_list[:limit], user_rank)
