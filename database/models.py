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

    def __repr__(self) -> str:
        return f"Exercise(number={self.number}, paragraph={self.paragraph}"

    @validates("paragraph")
    def validate_paragraph(self, key, value):
        """
        Ensure the exercise paragraph number do not contain "I"
        """
        return value.replace("I", "1").replace(" ", "")

    @classmethod
    def exists(cls, session: Session, exercise_data: Dict[str, str]) -> bool:
        """
        Check if an exercise already exists in the database
        Args:
            session (Session): SQLAlchemy session
            exercise_data (Dict[str, str]): exercise data
        Returns:
            bool: True if exercise exists, False otherwise
        """
        return (
            session.query(cls)
            .filter_by(
                number=exercise_data["number"], paragraph=exercise_data["paragraph"]
            )
            .first()
            is not None
        )

    @classmethod
    def save(cls, exercise_data: Dict[str, str]):
        """
        Save exercise to the database
        Args:
            exercise_data (Dict[str, str]): exercise data
        """
        exercise = Exercise(**exercise_data)
        with Session(bind=engine) as session:
            if not cls.exists(session, exercise_data):
                session.add(exercise)
                session.commit()
            else:
                print(f"{exercise} already exists in the DB")
                session.add(exercise)
                session.commit()
        return exercise
