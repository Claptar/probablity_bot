"Contains the Exercise class that represents an exercise from the book, stored in the database"
import logging
from typing import Dict, Type
from app.database.models.base import CommonAttributes
from app.database.models.paragraphs import Paragraph
from app.database.models.solutions import Solution
from app.database.models.sections import Section
from sqlalchemy.orm import relationship, Session
from sqlalchemy import Column, Integer, ForeignKey


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
        keywords = ["Exercise", "Theorem", "Example"]
        return any(keyword in self.contents for keyword in keywords)

    def refactor_contets(self) -> None:
        """
        Refactor exercise contents
        """
        self.contents = self.contents.replace("#", "")

    @classmethod
    def create(
        cls: Type["Exercise"],
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

        # check if the solution exists in the database
        if solution is None:
            logging.error(
                "Solution for exercise %s not found in the database",
                exercise_data["number"],
            )
            return None

        # create exercise object
        exercise = cls(
            paragraph_id=paragraph.id,
            solution_id=solution.id,
            **exercise_data,
        )

        # refactor the contents
        exercise.refactor_contets()

        # check if there are references in the exercise contents
        if exercise.check_references():
            logging.info("Creating a new exercise with data: %s", exercise_data)
            session.add(exercise)
            return exercise
        else:
            logging.error(
                "Exercise %s contents are invalid. Skipping the exercise",
                exercise_data["number"],
            )
            return None
