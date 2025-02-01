from app.database.models.base import CommonAttributes
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from app.database.models.paragraphs import Paragraph
from app.database.models.solutions import Solution
from app.database.models.sections import Section
from typing import Dict


class Exercise(CommonAttributes):
    """
    Represents an exercise from the book, stored in the database.
    """

    __tablename__ = "exercises"

    solution_id = Column(
        Integer, ForeignKey("solutions.id"), nullable=True, unique=True
    )

    paragraph = relationship("Paragraph", back_populates="exercise", uselist=False)
    solution = relationship("Solution", back_populates="exercise", uselist=False)

    def __repr__(self) -> str:
        return f"Exercise(number={self.number}, paragraph={self.paragraph}"

    def create(
        session,
        section_number: str,
        paragraph_number: str,
        exercise_data: Dict[str, str],
    ) -> "Exercise":
        """
        Create a new exercise in the database
        Args:
            session (Session): database session
            paragraph_id (int): paragraph id
            exercise_data (Dict[str, str]): exercise data
        Returns:
            Exercise: created exercise
        """
        section = session.query(Section).filter_by(number=section_number).one_or_none()
        paragraph = (
            session.query(Paragraph)
            .filter_by(section_id=section.id, number=paragraph_number)
            .one_or_none()
        )
        solution = (
            session.query(Solution)
            .filter_by(paragraph_id=paragraph.id, number=exercise_data["number"])
            .one_or_none()
        )
        exercise = Exercise(
            paragraph_id=paragraph.id,
            solution_id=solution.id if solution else None,
            **exercise_data,
        )
        session.add(exercise)
        return exercise
