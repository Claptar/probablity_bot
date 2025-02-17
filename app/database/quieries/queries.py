"A module for database queries"
import logging
from typing import Tuple, List, Dict, Any
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.database.models import (
    Exercise,
    User,
    Section,
    Paragraph,
    SelectedParagraph,
    SolvedExercise,
)
from app.database.quieries.utils import session_scope
from app.database.quieries.cache import cache_region


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

        # Get the paragraph IDs the user has selected
        selected_paragraph_ids = (
            session.query(SelectedParagraph.paragraph_id)
            .filter(SelectedParagraph.user_id == user.id)
            .subquery()
        )

        # get a random exercise that user hasn't solved yet
        if user.select_paragraphs:
            exercise = (
                session.query(Exercise)
                .join(Paragraph, Exercise.paragraph_id == Paragraph.id)
                .filter(Paragraph.id.in_(selected_paragraph_ids))
                .filter(~Exercise.id.in_(solved_exercise_ids))
                .order_by(func.random())
                .first()
            )
        else:
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


def get_current_exercise(telegram_id: str) -> Tuple[int, str] | None:
    """
    Get the last exercise that the user tried
    Args:
        telegram_id (str): Telegram's user id
    Returns:
        Tuple[int, str] | None: Exercise id and contents
    """
    with session_scope() as session:
        user = User.user_by_telegram_id(telegram_id, session)
        if user.last_trial_id is None:
            return None
        return user.last_trial_id, user.exercise.contents, user.exercise.paragraph.title


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


def update_user_score(user: User, session: Session) -> None:
    """
    Update the user's score
    Args:
        user (User): User object
    """
    total_score = (
        session.query(func.sum(Exercise.score))
        .join(SolvedExercise, SolvedExercise.exercise_id == Exercise.id)
        .filter(SolvedExercise.user_id == user.id)
        .scalar()
    )
    user.score = total_score or 0
    session.commit()


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
        update_user_score(user, session)
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


@cache_region.cache_on_arguments()
def get_sections() -> Dict[int, Dict[str, Any]]:
    """
    Get the list of sections
    Returns:
        Dict[int, Dict[str, Any]]: Dict with section id and section dictionary
    """
    with session_scope() as session:
        return Section.get_all_sections(session)


def get_selected_sections(telegram_id: str) -> Dict[str, Dict[str, Any]]:
    """
    Count paragraphs for all sections
    Args:
        telegram_id (str): Telegram's user id
        section_id (str): Section id
    Returns:
        Dict[str, Dict[str, Any]]: Dictionary with section id and section dictionary
    """
    with session_scope() as session:
        # get user by telegram id
        user = User.user_by_telegram_id(telegram_id, session)

        # get all sections
        sections = get_sections()

        # count selected paragraphs for each section
        return {
            section_id: {
                "selected_count": count_selected_paragraphs(
                    user.id, section_id, session
                ),
                **section,
            }
            for section_id, section in sections.items()
        }


def count_selected_paragraphs(user_id: int, section_id: str, session: Session) -> int:
    """
    Count the number of selected paragraphs by user id and section id
    Args:
        user_id (int): User id
        section_id (str): Section id
        session (Session): Database session
    Returns:
        int: Number of selected paragraphs
    """
    return (
        session.query(func.count(SelectedParagraph.paragraph_id))
        .join(Paragraph, Paragraph.id == SelectedParagraph.paragraph_id)
        .filter(
            SelectedParagraph.user_id == user_id, Paragraph.section_id == section_id
        )
        .scalar()
    )


@cache_region.cache_on_arguments()
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


def select_all_section_paragraphs(
    telegram_id: str, section_id: str, select=True
) -> None:
    """
    Select all paragraphs from the section
    Args:
        telegram_id (str): Telegram's user id
        section_id (str): Section id
    """
    paragraphs = get_section_paragraphs(section_id)
    with session_scope() as session:
        user = User.user_by_telegram_id(telegram_id, session)
        for paragraph_id in paragraphs.keys():
            if select:
                SelectedParagraph.select_paragraph(user.id, paragraph_id, session)
            else:
                SelectedParagraph.unselect_paragraph(user.id, paragraph_id, session)


def get_selected_section_paragraphs(
    telegram_id: str, section_id: str
) -> Dict[int, Dict[str, Any]]:
    """
    Get the selected paragraphs by user id and section id
    Args:
        telegram_id (str): Telegram's user id
        section_id (str): Section id
    Returns:
        Dict[int, Dict[str, Any]]: Dict of paragraphs
    """
    with session_scope() as session:
        user = User.user_by_telegram_id(telegram_id, session)
        paragraphs = get_section_paragraphs(section_id)
        return {
            paragraph_id: {
                "selected": SelectedParagraph.get_selected_paragraph(
                    user.id, paragraph_id, session
                )
                is not None,
                **paragraph,
            }
            for paragraph_id, paragraph in paragraphs.items()
        }


@cache_region.cache_on_arguments()
def count_all_exercises() -> Dict[int, Dict[str, Any]]:
    """
    Count the number of all exercises in each section
    Returns:
        Dict[int, Dict[str, Any]]: section data with the number of exercises
    """
    with session_scope() as session:
        # get all sections
        sections = get_sections()

        # count all exercises for each section
        total_exercises = dict(
            session.query(Section.id, func.count(Exercise.id))
            .join(Paragraph, Paragraph.section_id == Section.id)
            .join(Exercise, Exercise.paragraph_id == Paragraph.id)
            .group_by(Section.id)
            .all()
        )
        return {
            section_id: {"total": total_exercises[section_id], **section}
            for section_id, section in sections.items()
        }


def count_solved_exercises(telegram_id: str) -> List[Dict[str, int]]:
    """
    Count the number of solved exercises by user id for each section
    Args:
        telegram_id (str): Telegram's user id
    Returns:
        List[Dict[str, int]]: Number of solved exercises for each section
    """
    with session_scope() as session:
        # get user by telegram id
        user = User.user_by_telegram_id(telegram_id, session)

        # get a number of all exercises for each section
        exercise_numbers = count_all_exercises()

        # count solved exercises
        solved_count = dict(
            session.query(Section.id, func.count(Exercise.id))
            .join(Paragraph, Paragraph.section_id == Section.id)
            .join(Exercise, Exercise.paragraph_id == Paragraph.id)
            .join(SolvedExercise, SolvedExercise.exercise_id == Exercise.id)
            .filter(SolvedExercise.user_id == user.id)
            .group_by(Section.id)
            .all()
        )

        return [
            {"solved": solved_count.get(section_id, 0), **section}
            for section_id, section in exercise_numbers.items()
        ]
