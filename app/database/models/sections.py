"Contains the Section class that represents a section from the book, stored in the database"
from typing import Type
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import Session, relationship
from app.database.models.base import Base


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
    selected_sections = relationship("SelectedSections", back_populates="section")

    def __repr__(self) -> str:
        return f"Section(number={self.number}, title={self.title})"

    @classmethod
    def section_by_number(
        cls: Type["Section"], number: str, session: Session
    ) -> "Section":
        """
        Get the user by telegram id
        Args:
            number (str): section number
            session (Session): SQLAlchemy session
        Returns:
            User: User object
        """
        section = session.query(cls).filter_by(number=number).one_or_none()
        if section:
            return section
        else:
            raise ValueError(f"Section with number {number} not found in the database")
