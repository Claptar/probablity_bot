"Contains the SelectedSections class that represents a sections selected by user in the database"
from typing import Type
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.models.base import Base
from app.database.models.users import User
from app.database.models.sections import Section
from app.database.quieries.utils import session_scope


class SelectedSections(Base):
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

    @classmethod
    def add_selected_section(
        cls: Type["SelectedSections"], telegram_id: int, section_number: str
    ) -> None:
        """
        Add a new solved exercise to the database
        Args:
            user_id (int): user id
            section (str): section number
        """
        with session_scope() as session:
            # get user by telegram id
            user = User.user_by_telegram_id(telegram_id=telegram_id, session=session)

            # get section id by section number
            section = Section.section_by_number(number=section_number)

            # create a new solved exercise
            selected_section = cls(user_id=user.id, section_id=section.id)
            session.add(selected_section)

            # update user's status
            user.select_sections = True
