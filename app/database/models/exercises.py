"Contains the Exercise class that represents an exercise from the book, stored in the database"
import logging
from typing import Dict, Type
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, Integer, ForeignKey
from app.database.models.base import CommonAttributes
from app.database.models.paragraphs import Paragraph
from app.database.models.solutions import Solution
from app.database.models.sections import Section


class Exercise(CommonAttributes):
    """
    Represents an exercise from the book, stored in the database.
    """

    __tablename__ = "exercises"

    solution_id = Column(
        Integer, ForeignKey("solutions.id"), nullable=False, unique=True
    )
    score = Column(Integer, default=1)

    paragraph = relationship("Paragraph", back_populates="exercise", uselist=False)
    solution = relationship("Solution", back_populates="exercise", uselist=False)
    solved_exercises = relationship("SolvedExercise", back_populates="exercise")
    table = relationship("Table", back_populates="exercise", uselist=False)

    def __repr__(self) -> str:
        return f"Exercise(number={self.number}, paragraph={self.paragraph}"

    def check_references(self) -> bool:
        """
        Check if there are any references in the exercise contents
        Args:
            session (Session): database session
        Returns:
            bool: True if the contents are valid, False otherwise
        """
        keywords = ["Theorem", "Example"]
        return any(keyword in self.contents for keyword in keywords)

    def refactor_contets(self) -> None:
        """
        Refactor exercise contents
        """
        self.contents = self.contents.replace("#", "")
