"Contains the Solution class that represents an exercise from the book, stored in the database"
import logging
from app.database.models.base import CommonAttributes
from sqlalchemy.orm import relationship
from sqlalchemy.exc import NoResultFound
from sqlalchemy import Column, Integer, ForeignKey


class Solution(CommonAttributes):
    """
    Represents an exercise from the book, stored in the database.
    """

    __tablename__ = "solutions"

    paragraph = relationship("Paragraph", back_populates="solution", uselist=False)
    exercise = relationship("Exercise", back_populates="solution", uselist=False)

    def __repr__(self) -> str:
        return f"Solution(number={self.number}, paragraph={self.paragraph}"

    @classmethod
    def solution_by_paragraph_and_number(
        cls, number: str, paragraph_id: int, session
    ) -> "Solution":
        """
        Get the user by telegram id
        Args:
            number (str): Solution number
            paragraph_id (int): Paragraph id
            session (Session): SQLAlchemy session
        Returns:
            User: User object
        """
        solution = (
            session.query(cls)
            .filter_by(paragraph_id=paragraph_id, number=number)
            .one_or_none()
        )
        if not solution:
            logging.warn("Solution with number %s not found in the database", number)
        return solution
