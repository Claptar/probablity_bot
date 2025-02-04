"Contains the Section class that represents a section from the book, stored in the database"
from typing import Dict, Optional
from app.database.models.base import Base
from sqlalchemy import (
    Integer,
    String,
    Column,
    ForeignKey,
)
from sqlalchemy.orm import Session, relationship
from sqlalchemy.exc import IntegrityError


class Section(Base):
    """
    Represents a table with sections stored in the database

    Attributes:
        id: Unique identifier
        number: Section number
        title: Section title
    """

    __tablename__ = "sections"

    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)

    paragraph = relationship("Paragraph", back_populates="section")
