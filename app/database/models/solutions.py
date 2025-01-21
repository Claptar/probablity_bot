from app.database.models.base import CommonAttributes
from sqlalchemy.orm import relationship
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
