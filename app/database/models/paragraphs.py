from typing import Dict, Optional
from app.database.models.base import Base
from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.exc import IntegrityError


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
