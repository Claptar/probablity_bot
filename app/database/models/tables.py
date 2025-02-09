"Contains the Table class that represents a table from the book, stored in the database"
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from app.database.models.base import Base


class Table(Base):
    """
    Represents a table from the book, stored in the database
    Attributes:
        id: Unique identifier
        number: Table number
        contents: Table contents
        section_id: Section id
    """

    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    contents = Column(String, nullable=False)
    section_id = Column(Integer, nullable=False)

    section = relationship("Section", back_populates="table")
    exercises = relationship("Exercise", back_populates="table", uselist=True)

    def __repr__(self) -> str:
        return f"Table(number={self.number}, section_id={self.section_id})"
