"Contains the Section class that represents a section from the book, stored in the database"
from typing import Type, Dict, Any, List
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import Session, relationship
from sqlalchemy.exc import NoResultFound
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
    selected_sections = relationship("SelectedSection", back_populates="section")
    tables = relationship("Table", back_populates="section", uselist=True)

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
        if not section:
            raise NoResultFound(
                f"Section with number {number} not found in the database"
            )
        return section

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the section to a dictionary
        Returns:
            Dict[str, Any]: Section dictionary
        """
        return {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "paragraph_count": len(self.paragraph),
        }

    @classmethod
    def get_all_sections(
        cls: Type["Section"], session: Session
    ) -> Dict[int, Dict[str, Any]]:
        """
        Get all sections
        Args:
            session (Session): SQLAlchemy session
        Returns:
            Dict[int, Dict[str, Any]]: Dictionary with section id and section dictionary
        """
        # Get all sections
        sections = session.query(cls).all()

        # Check if sections were found
        if not sections:
            raise ValueError("No sections found in the database")

        # Create a list with all sections
        sections_dict = {section.id: section.to_dict() for section in sections}
        return sections_dict
