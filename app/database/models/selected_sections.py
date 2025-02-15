"Contains the SelectedSection class that represents a sections selected by user in the database"
from typing import Dict
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Session
from app.database.models.base import Base


class SelectedSection(Base):
    """
    Represents a table to store sections selected by users.
    """

    __tablename__ = "selected_sections"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=False)

    user = relationship("User", back_populates="selected_sections")
    section = relationship("Section", back_populates="selected_sections")

    def __repr__(self) -> str:
        return (
            f"SelectedSections(user_id={self.user_id}, section_id_id={self.section_id})"
        )

    def __str__(self) -> str:
        return f"Selected section {self.section_id} selected by user {self.user_id}"
    
    def to_dict(self) -> Dict:
        """
        Convert the object to a dictionary
        Returns:
            Dict: Dictionary representation of the object
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "section_id": self.section_id,
        }

    @classmethod
    def get_selected_sections(cls, user_id: int, session: Session) -> list:
        """
        Get the selected sections by user id
        Args:
            user_id (int): User id
            session (Session): SQLAlchemy session
        Returns:
            list: List of selected sections
        """
        return session.query(cls).filter(cls.user_id == user_id).all()

    @classmethod
    def get_selected_section(
        cls, user_id: int, section_id: int, session: Session
    ) -> "SelectedSection":
        """
        Get the selected section by user id and section id
        Args:
            user_id (int): User id
            section_id (int): Section id
            session (Session): SQLAlchemy session
        Returns:
            SelectedSection: Selected section object
        """
        return (
            session.query(cls)
            .filter(cls.user_id == user_id, cls.section_id == section_id)
            .one_or_none()
        )
