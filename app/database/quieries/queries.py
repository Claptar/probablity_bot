"A module for database queries"
import logging
from typing import Tuple, List, Dict, Any
from sqlalchemy.sql.expression import func
from sqlalchemy.exc import NoResultFound
from app.database.models import (
    Exercise,
    User,
    Section,
    SelectedSection,
    Paragraph,
    SelectedParagraph,
)
from app.database.quieries.utils import session_scope


def get_random_exercise(
    first_name: str, telegram_id: str, username: str
) -> Tuple[int, str]:
    """
    Retrieve a random exercise from the database.
    Args:
        first_name (str): user's first name
        telegram_id (int): user's telegram_id
        username (str): user's username
    Returns:
        Tuple[int, str]: exercise id and contents
    """
    with session_scope() as session:
        # get user
        user = User.user_by_telegram_id(telegram_id, session)

        # Extract the IDs of solved exercises
        solved_exercise_ids = [
            solved_exercise.exercise_id for solved_exercise in user.solved_exercises
        ]

        # get a random exercise that user hasn't solved yet
        exercise = (
            session.query(Exercise)
            .filter(~Exercise.id.in_(solved_exercise_ids))
            .order_by(func.random())
            .first()
        )

        if exercise is None:
            error_message = "No unsolved exercises found for the user"
            logging.error(error_message)
            raise NoResultFound(error_message)

        return exercise.id, exercise.contents, exercise.paragraph.title


def update_users_exercise(telegram_id: str, exercise_id: int) -> None:
    """
    Update the last exercise that the user tried
    Args:
        telegram_id (int): Telegram's user id
        exercise_id (int): Exercise id
    """
    with session_scope() as session:
        user = User.user_by_telegram_id(telegram_id, session)
        user.last_trial_id = exercise_id
        session.commit()


def get_user_leaderboard(telegram_id: str) -> str:
    """
    Get the top users based on their scores
    Args:
        telegram_id (str): Telegram's user id
    Returns:
        str: Leaderboard text
    """
    with session_scope() as session:
        return User.user_leaderboard(telegram_id, session)


def get_user_score(telegram_id: str) -> int:
    """
    Get the user's score
    Args:
        telegram_id (str): Telegram's user id
    Returns:
        int: User's score
    """
    with session_scope() as session:
        user = User.user_by_telegram_id(telegram_id, session)
        return user.score


def user_exercise_soluiton(telegram_id: str) -> str:
    """
    Get the solution of the last exercise that the user tried
    Args:
        telegram_id (str): Telegram's user id
    Returns:
        str: Solution text of the last exercise
    """
    with session_scope() as session:
        user = User.user_by_telegram_id(telegram_id, session)
        if user.last_trial_id is None:
            raise NoResultFound("User has not tried any exercise yet")
        return user.exercise.solution.contents


def get_sections() -> Dict[int, str]:
    """
    Get the list of sections
    Returns:
        Dict[int, str]: Dict with section id and title
    """
    with session_scope() as session:
        return Section.get_all_sections(session)


def get_selected_sections(telegram_id: str) -> List[int]:
    """
    Get the selected sections by user id
    Args:
        telegram_id (str): Telegram's user id
    Returns:
        List[int]: List of selected sections' ids
    """
    with session_scope() as session:
        user = User.user_by_telegram_id(telegram_id, session)
        selected_sections = SelectedSection.get_selected_sections(user.id, session)
        return (
            [section.section_id for section in selected_sections]
            if selected_sections
            else []
        )


def get_section_paragraphs(section_id: str) -> List[Dict[str, Any]]:
    """
    Get the list of paragraphs
    Args:
        section_id (str): Section id
    Returns:
        List[Dict[str, Any]]: List of paragraphs
    """
    with session_scope() as session:
        return Paragraph.get_section_paragraphs(section_id, session)


def get_selected_section_paragraphs(telegram_id: str, section_id: str) -> List[int]:
    """
    Get the selected paragraphs by user id and section id
    Args:
        telegram_id (str): Telegram's user id
        section_id (str): Section id
    Returns:
        List[int]: List of selected paragraphs' ids
    """
    with session_scope() as session:
        user = User.user_by_telegram_id(telegram_id, session)

        # get user's selected paragraphs, fro each paragraph get section_id and filter only paragraphs from specified section
        selected_paragraphs = (
            session.query(Paragraph)
            .join(SelectedParagraph, SelectedParagraph.paragraph_id == Paragraph.id)
            .filter(
                SelectedParagraph.user_id == user.id, Paragraph.section_id == section_id
            )
            .all()
        )
        return [paragraph.id for paragraph in selected_paragraphs]
