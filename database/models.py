import config
from typing import Dict
from sqlalchemy import create_engine, Integer, String, Column, ForeignKey
from sqlalchemy.orm import declarative_base, Session, validates, relationship
from sqlalchemy.exc import IntegrityError, NoResultFound


Base = declarative_base()

engine = create_engine(config.DB_URL)


class CommonAttributes(Base):
    """
    Represents a table with parsed book, stored in the database

    Attributes:
        id: Unique identifier
        number: Exercise number within the paragraph
        paragraph: Paragraph number (e.g., "1.2")
        contents: The exercise question/prompt
        solution_text: The solution to the exercise
    """

    __abstract__ = True  # This class will not be mapped to a table

    id = Column(Integer, primary_key=True)
    number = Column(String, nullable=False)
    paragraph = Column(String, nullable=False)
    contents = Column(String, nullable=False)

    @validates("paragraph")
    def validate_paragraph(self, key, value):
        return value.replace("I", "1").replace(" ", "").replace("O", "0")

    @classmethod
    def exists(cls, session: Session, data: Dict[str, str]) -> bool:
        return (
            session.query(cls)
            .filter_by(number=data["number"], paragraph=data["paragraph"])
            .first()
        )

    @classmethod
    def save(cls, data: Dict[str, str]):
        """
        Save exercise to the database
        Args:
            exercise_data (Dict[str, str]): exercise data
        """
        instance = cls(**data)
        with Session(bind=engine) as session:
            if cls.exists(session, data):
                raise IntegrityError(
                    f"{instance} already exists in the DB", params=None, orig=None
                )
            session.add(instance)
            session.commit()
        return instance


class Exercise(CommonAttributes):
    """
    Represents an exercise from the book, stored in the database.
    """

    __tablename__ = "exercises"

    solution = relationship("Solution", back_populates="exercise", uselist=False)

    def __repr__(self) -> str:
        return f"Exercise(number={self.number}, paragraph={self.paragraph}"


class Solution(CommonAttributes):
    """
    Represents an exercise from the book, stored in the database.
    """

    __tablename__ = "solutions"

    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    exercise = relationship("Exercise", back_populates="solution")

    def __repr__(self) -> str:
        return f"Solution(number={self.number}, paragraph={self.paragraph}"

    @classmethod
    def save(cls, data: Dict[str, str]):
        """
        Save exercise to the database
        Args:
            exercise_data (Dict[str, str]): exercise data
        """
        with Session(bind=engine) as session:
            exercise = (
                session.query(Exercise)
                .filter_by(number=data["number"], paragraph=data["paragraph"])
                .one_or_none()
            )
            if exercise:
                solution = cls(exercise_id=exercise.id, **data)
                if cls.exists(session, data):
                    raise IntegrityError(
                        f"{solution} already exists in the DB", params=None, orig=None
                    )
                session.add(solution)
                session.commit()
                return solution
            else:
                raise NoResultFound(
                    f"Exercise with number {data['number']} and paragraph {data['paragraph']} not found"
                )
