"Contains the Selected{aragraphs class that represents a paragraphs selected by user in the database"
from typing import Type
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.models.base import Base
from app.database.models.users import User
from app.database.models.paragraphs import Paragraph
from app.database.quieries.utils import session_scope


class SelectedParagraphs(Base):
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
        return f"SelectedParagraphs(user_id={self.user_id}, paragraph_id_id={self.paragraph_id})"

    @classmethod
    def add_selected_paragraph(
        cls: Type["SelectedParagraphs"], telegram_id: int, paragraph_number: str
    ) -> None:
        """
        Add a new solved exercise to the database
        Args:
            user_id (int): user id
            paragraph (str): paragraph number
        """
        with session_scope() as session:
            # get user by telegram id
            user = User.user_by_telegram_id(telegram_id=telegram_id, session=session)

            # get paragraph id by paragraph number
            paragraph = Paragraph.paragraph_by_number(number=paragraph_number)

            # create a new solved exercise
            selected_paragraph = cls(user_id=user.id, paragraph_id=paragraph.id)
            session.add(selected_paragraph)

            # update user's status
            user.select_paragraphs = True
