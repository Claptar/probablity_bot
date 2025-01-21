from app.database.models.base import CommonAttributes
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey


class Exercise(CommonAttributes):
    """
    Represents an exercise from the book, stored in the database.
    """

    __tablename__ = "exercises"

    solution_id = Column(Integer, ForeignKey("solutions.id"), nullable=False, unique=True)

    paragraph = relationship("Paragraph", back_populates="exercise", uselist=False)
    solution = relationship("Solution", back_populates="exercise", uselist=False)

    def __repr__(self) -> str:
        return f"Exercise(number={self.number}, paragraph={self.paragraph}"
