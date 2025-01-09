import config
from typing import Dict
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import declarative_base, Session, validates


Base = declarative_base()

engine = create_engine(config.DB_URL)


class Exercise(Base):
    """
    Represents an exercise from the book, stored in the database.

    Attributes:
        id: Unique identifier
        number: Exercise number within the paragraph
        paragraph: Paragraph number (e.g., "1.2")
        contents: The exercise question/prompt
        solution_text: The solution to the exercise
    """

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    paragraph = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    solution = Column(String, default="No solution")

    def __repr__(self) -> str:
        return f"Exercise(number={self.number}, paragraph={self.paragraph})"

    @validates("number")
    def validate_number(self, key, value):
        """
        Ensure the exercise number is a positive integer.
        """
        return value.replace("I", "1")

    @classmethod
    def save(cls, exercise_data: Dict[str, str]):
        """
        Save exercise to the database
        Args:
            exercise_data (Dict[str, str]): exercise data
        """
        exercise = Exercise(**exercise_data)
        with Session(bind=engine) as session:
            session.add(exercise)
        return exercise
