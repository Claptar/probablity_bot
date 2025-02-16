"Contains the SelectedParagraph class that represents a paragraphs selected by user in the database"
import logging
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

    @classmethod
    def get_selected_paragraph(
        cls, user_id: int, paragraph_id: int, session: Session
    ) -> "SelectedParagraph":
        """
        Get a selected paragraph by user id
        Args:
            user_id (int): User id
            paragraph_id (int): Paragraph id
            session (Session): Database session
        Returns:
            SelectedParagraph: Selected paragraph
        """
        return (
            session.query(cls)
            .filter_by(user_id=user_id, paragraph_id=paragraph_id)
            .one_or_none()
        )

    @classmethod
    def select_paragraph(
        cls, user_id: int, paragraph_id: int, session: Session
    ) -> None:
        """
        Select a paragraph by user id
        Args:
            user_id (int): User id
            paragraph_id (int): Paragraph id
            session (Session): Database session
        """
        # Check if the paragraph is already selected
        selected_paragraph = cls.get_selected_paragraph(user_id, paragraph_id, session)
        if selected_paragraph:
            logging.info(
                "Paragraph %s is already selected for user %s", paragraph_id, user_id
            )
        else:
            logging.info("Selecting paragraph %s for user %s", paragraph_id, user_id)
            selected_paragraph = cls(user_id=user_id, paragraph_id=paragraph_id)
            session.add(selected_paragraph)
            session.commit()

    @classmethod
    def unselect_paragraph(
        cls, user_id: int, paragraph_id: int, session: Session
    ) -> None:
        """
        Unselect a paragraph by user id
        Args:
            user_id (int): User id
            paragraph_id (int): Paragraph id
            session (Session): Database session
        """
        # Check if the paragraph is selected
        selected_paragraph = cls.get_selected_paragraph(user_id, paragraph_id, session)
        if selected_paragraph:
            logging.info("Unselecting paragraph %s for user %s", paragraph_id, user_id)
            session.delete(selected_paragraph)
            session.commit()
        else:
            logging.info(
                "Paragraph %s is not selected for user %s", paragraph_id, user_id
            )
