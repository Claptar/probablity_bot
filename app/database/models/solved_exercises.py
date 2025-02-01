from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.models.base import Base


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
