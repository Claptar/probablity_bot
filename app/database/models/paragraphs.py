"Contains the Paragraph class that represents a section from the book, stored in the database"
from typing import Dict, Type
from app.database.models.base import Base
from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.database.models.sections import Section


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

    @classmethod
    def create(
        cls: Type["Paragraph"],
        session: Session,
        section_number: int,
        paragraph_data: Dict[str, str],
    ) -> None:
        """
        Create a paragraph in the database
        Args:
            session (Session): database session
            section_number (int): section number
            paragraph_data (Dict[str, str]): paragraph data
        Returns:
            Paragraph: paragraph object
        """
        section = session.query(Section).filter_by(number=section_number).one_or_none()
        if not section:
            raise NoResultFound(f"Section {section_number} not found in the database")
        paragraph = cls(section_id=section.id, **paragraph_data)
        session.add(paragraph)
        session.commit()
        return paragraph
