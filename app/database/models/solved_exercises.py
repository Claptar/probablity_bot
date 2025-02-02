from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.models.base import Base
from app.database.models.users import User
from app.database.quieries.utils import session_scope
from typing import Type


class SolvedExercise(Base):
    """
    Represents a table to store solved exercises by users.
    """

    __tablename__ = "solved_exercises"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)

    user = relationship("User", back_populates="solved_exercises")
    exercise = relationship("Exercise", back_populates="solved_exercises")

    def __repr__(self) -> str:
        return f"SolvedExercise(user_id={self.user_id}, exercise_id={self.exercise_id})"

    @classmethod
    def add_user_solution(cls: Type["SolvedExercise"], telegram_id: int) -> None:
        """
        Add a new solved exercise to the database
        Args:
            user_id (int): user id
        """
        with session_scope() as session:
            # get user by telegram id
            user = session.query(User).filter_by(telegram_id=telegram_id).one_or_none()

            # create a new solved exercise
            solved_exercise = cls(user_id=user.id, exercise_id=user.last_trial_id)
            session.add(solved_exercise)

            # update user's score and remove last trial id
            user.score += user.exercise.score
            user.last_trial_id = None
