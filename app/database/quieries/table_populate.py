" Queries to populate database tables "
import logging
from sqlalchemy.orm import Session
from app.database.models import (
    Exercise,
    Solution,
    Section,
    Paragraph,
    User,
    SolvedExercise,
    SelectedParagraph,
)
from app.database.quieries.utils import session_scope
from app.database.quieries.queries import update_user_score


def add_user(first_name: str, telegram_id: str, username: str) -> User:
    """
    Create a new user in the database.
    Args:
        first_name (str): first name
        telegram_id (str): telegram id
        username (str): username

    Raises:
        ValueError: if telegram id is not provided

    Returns:
        User:
    """
    logging.info("Creating a new user")

    # check if there is telegram_id in the user_data
    if telegram_id is None:
        raise ValueError("Telegram id is required to create a user")

    with session_scope() as session:
        # check if the user already exists in the database
        user = session.query(User).filter_by(telegram_id=telegram_id).one_or_none()
        if user:
            logging.warning(
                "User %s exists in the database. Updating the user data", user
            )
            user.first_name = first_name
            user.username = username
            logging.info("Updated user data: %s", user)
        else:
            user = User(
                first_name=first_name, telegram_id=telegram_id, username=username
            )
            session.add(user)
        session.commit()


def add_paragraph(
    section_number: str, paragraph_data: str, session: Session
) -> Paragraph:
    """
    Create a paragraph and save it to the database.
    Args:
        section_number (str): section number
        paragraph_data (str): paragraph data
        session (Session): database session
    Returns:
        Paragraph: created paragraph
    """
    section = Section.section_by_number(section_number, session)
    paragraph = Paragraph(section_id=section.id, **paragraph_data)
    session.add(paragraph)
    return paragraph


def add_exercise(
    section_number: str, paragraph_number: str, exercise_data: str, session: Session
) -> Exercise:
    """
    Create an exercise and save it to the database.
    Args:
        section_number (str): section number
        paragraph_number (str): paragraph number
        exercise_data (str): exercise data
        session (Session): database session
    Returns:
        Exercise: created exercise
    """
    # get section, paragraph and solution objects from DB
    section = Section.section_by_number(section_number, session)
    paragraph = Paragraph.paragraph_by_section_and_number(
        paragraph_number, section.id, session
    )
    solution = Solution.solution_by_paragraph_and_number(
        exercise_data["number"], paragraph.id, session
    )

    # check if the solution exists in the database
    if solution is None:
        logging.error(
            "Solution for exercise %s not found in the database",
            exercise_data["number"],
        )
        return None

    # create exercise object
    exercise = Exercise(
        paragraph_id=paragraph.id, solution_id=solution.id, **exercise_data
    )

    # refactor the contents
    exercise.refactor_contets()
    if exercise.check_references():
        logging.warning(
            "Exercise %s contents are invalid. Skipping the exercise",
            exercise_data["number"],
        )
    # add the exercise to the table
    logging.info("Creating a new exercise with data: %s", exercise_data)
    session.add(exercise)


def add_solved_exercise(telegram_id: str):
    """
    Add a solved exercise to the database.
    Args:
        user_id (int): user id
    """
    with session_scope() as session:
        # get user by telegram id
        user = User.user_by_telegram_id(telegram_id, session)

        # create solved exercise object
        solved_exercise = SolvedExercise(
            user_id=user.id, exercise_id=user.last_trial_id
        )
        session.add(solved_exercise)

        logging.info("%s solved the exercise %s", user, user.last_trial_id)

        # set the last trial to None
        user.last_trial_id = None
        session.commit()


def add_selected_paragraph(telegram_id: str, paragraph_id: int):
    """
    Add a selected paragraph to the database.
    Args:
        telegram_id (str): telegram id
        paragraph_id (int): paragraph id
    """
    with session_scope() as session:
        # get user by telegram id
        user = User.user_by_telegram_id(telegram_id, session)

        # check if the paragraph is already selected
        selected_paragraph = (
            session.query(SelectedParagraph)
            .filter_by(user_id=user.id, paragraph_id=paragraph_id)
            .one_or_none()
        )

        # if the paragraph is already selected remove it
        if selected_paragraph:
            session.delete(selected_paragraph)
            logging.info("Removed paragraph %s from user %s", paragraph_id, user)
        else:
            # create selected paragraph object
            selected_paragraph = SelectedParagraph(
                user_id=user.id, paragraph_id=paragraph_id
            )
            session.add(selected_paragraph)
            logging.info("Added paragraph %s to user %s", paragraph_id, user)
        session.commit()

        # get the selected paragraphs for the user
        selected_paragraphs = user.selected_paragraphs
        logging.info(
            "There is %s paragraphs for user %s", len(selected_paragraphs), user
        )

        # change user's state to select paragraphs
        update_user_score(user, session)
        user.select_paragraphs = len(selected_paragraphs) > 0
        session.commit()
