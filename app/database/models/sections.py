"Contains the Section class that represents a section from the book, stored in the database"
from typing import Type
from string import Template
from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import Session, relationship
from sqlalchemy.exc import NoResultFound
from app.database.models.base import Base
from app.database.quieries import cache_region


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

    @classmethod
    def get_all_sections(cls: Type["Section"], session: Session) -> str:
        """
        Get all sections
        Args:
            session (Session): SQLAlchemy session
        Returns:
            List[Section]: List of Section objects
        """
        # Get all sections
        sections = session.query(cls).all()

        # Check if sections were found
        if not sections:
            raise ValueError("No sections found in the database")

        # Create a message with all sections
        # section_list = [f"{section.title}:\t" for section in sections]
        return sections
