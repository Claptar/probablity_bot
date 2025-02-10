"Contains the SelectedSection class that represents a sections selected by user in the database"
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
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
