"A module that contains the Base and CommonAttributes classes"
from sqlalchemy import (
    Integer,
    String,
    Column,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class CommonAttributes(Base):
    """
    Represents a table with exercises stored in the database. The exercises
    are parsed from the book.

    Attributes:
        id: Unique identifier
        number: The exercise number
        paragraph_id: The paragraph that the exercise belongs to
        contents: The exercise question/prompt
    """

    __abstract__ = True  # This class will not be mapped to a table

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    paragraph_id = Column(Integer, ForeignKey("paragraphs.id"))
    contents = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("number", "paragraph_id", name="_number_paragraph_uc"),
    )
