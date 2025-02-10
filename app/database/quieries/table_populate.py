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
)
from app.database.quieries.utils import session_scope


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


def add_solved_exercise(user_id: int):
    """
    Add a solved exercise to the database.
    Args:
        user_id (int): user id
    """
    with session_scope() as session:
        # get user by telegram id
        user = User.user_by_telegram_id(user_id, session)

        # create solved exercise object
        solved_exercise = SolvedExercise(
            user_id=user.id, exercise_id=user.last_trial_id
        )
        session.add(solved_exercise)

        logging.info("%s solved the exercise %s", user, user.last_trial_id)

        # set the last trial to None
        user.last_trial_id = None
        session.commit()
