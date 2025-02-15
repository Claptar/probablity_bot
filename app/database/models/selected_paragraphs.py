"Contains the SelectedParagraph class that represents a paragraphs selected by user in the database"
from typing import Dict, List, Any
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Session
from app.database.models.base import Base


class SelectedParagraph(Base):
    """
    Represents a table to store paragraphs selected by users.
    """

    __tablename__ = "selected_paragraphs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    paragraph_id = Column(Integer, ForeignKey("paragraphs.id"), nullable=False)

    user = relationship("User", back_populates="selected_paragraphs")
    paragraph = relationship("Paragraph", back_populates="selected_paragraphs")

    def __repr__(self) -> str:
        return f"SelectedParagraph(user_id={self.user_id}, paragraph_id_id={self.paragraph_id})"

    def __str__(self) -> str:
        return f"Selected paragraph {self.paragraph_id} selected by user {self.user_id}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the object to a dictionary
        Returns:
            Dict[str, Any]: Dictionary representation of the object
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "paragraph_id": self.paragraph_id,
        }
