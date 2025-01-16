from app import config
from typing import Dict, Optional
from sqlalchemy import (
    create_engine,
    Integer,
    String,
    Column,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Session, validates, relationship
from sqlalchemy.exc import IntegrityError, NoResultFound


engine = create_engine(config.DB_URL)


class Base(DeclarativeBase):
    pass


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

    __table_args__ = (
        UniqueConstraint("number", "paragraph", name="_number_paragraph_uc"),
    )

    @classmethod
    def get_by_number_and_paragraph(
        cls, session: Session, number: str, paragraph: str
    ) -> Optional["CommonAttributes"]:
        """
        Retrieve an instance by number and paragraph.
        """
        return (
            session.query(cls)
            .filter_by(number=number, paragraph=paragraph)
            .one_or_none()
        )

    @classmethod
    def create(cls, session: Session, data: Dict[str, str]) -> "CommonAttributes":
        """
        Create a new instance if it doesn't exist.
        """
        instance = cls(**data)
        session.add(instance)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise IntegrityError(
                f"{instance} already exists in the DB", params=None, orig=None
            )
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
