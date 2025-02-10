"Contains the Paragraph class that represents a section from the book, stored in the database"
from typing import Type
from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.orm.exc import NoResultFound
from app.database.models.base import Base


class Paragraph(Base):
    """
    Represents a table with paragraphs stored in the database

    Attributes:
        id: Unique identifier
        section_id: Section id that the paragraph belongs to
        number: Paragraph number
        title: Paragraph title
        contents: Paragraph contents
    """

    __tablename__ = "paragraphs"

    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    contents = Column(String)

    __table_args__ = (
        UniqueConstraint("section_id", "number", name="_paragraph_section_number_uc"),
    )

    section = relationship("Section", back_populates="paragraph", uselist=False)
    exercise = relationship("Exercise", back_populates="paragraph")
    solution = relationship("Solution", back_populates="paragraph")
    selected_paragraphs = relationship("SelectedParagraph", back_populates="paragraph")

    @classmethod
    def paragraph_by_section_and_number(
        cls: Type["Paragraph"], number: str, section_id: int, session: Session
    ) -> "Paragraph":
        """
        Get the user by telegram id
        Args:
            number (str): Paragraph number
            section_id (int): Section id
            session (Session): SQLAlchemy session
        Returns:
            User: User object
        """
        paragraph = (
            session.query(cls)
            .filter_by(section_id=section_id, number=number)
            .one_or_none()
        )
        if not paragraph:
            raise NoResultFound(
                f"Paragraph with number {number} not found in the database"
            )
        return paragraph
