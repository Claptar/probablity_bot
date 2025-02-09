" Module to populate the database with sections, paragraphs, solutions and exercises. "
from typing import Iterator, Tuple
from sqlalchemy.orm import Session
from app import config
from app.parsers import parse_sections, get_paragraphs, parse_exercises, get_exercises
from app.database.models import Exercise, Solution, Section, Paragraph
from app.database.quieries.utils import session_scope
from app.database.quieries.database_init import initialize_database
from app.database.quieries.table_populate import add_paragraph


def populate_sections(text: str, session: Session) -> None:
    """
    Parse sections from a solution mannual and save them to the database.
    Args:
        text (str): solution mannual's text in markdown format
        session (Session): database session
    """
    for section_match in parse_sections(text):
        section = Section(**section_match.groupdict())
        session.add(section)


def populate_solutions_and_paragraphs(text: str) -> None:
    """
    Parse solutions and paragraphs from a solution mannual and save them to the database.
    Args:
        text (str): solution mannual's text in markdown format
    """
    for section_number, solution_section, paragraph_data in get_paragraphs(text):
        with session_scope() as session:
            # add paragraph to the table
            paragraph = add_paragraph(section_number, paragraph_data, session)

            # add solutions from paragraph to the table
            for solution_match in parse_exercises(solution_section):
                solution = Solution(
                    paragraph_id=paragraph.id, **solution_match.groupdict()
                )
                session.add(solution)

            # commit the session
            session.commit()


def populate_exercises(text: str) -> None:
    """
    Parse exercises from a book and save them to the database
    Args:
        text (str): text in markdown format
    """
    for section_number, paragraph_number, exercise_data in get_exercises(text):
        with session_scope() as session:
            exercise = Exercise.create(
                session, section_number, paragraph_number, exercise_data
            )


def process_solution_mannual(filepath: str) -> None:
    """
    Parse sollution mannually from a file and save exercises, paragrapgs
    and sections to the database.
    Args:
        filepath (str): file path to the book in markdown extension
    """
    # Read the book
    with open(filepath, "r") as file:
        text = file.read()

    # Populate sections
    with session_scope() as session:
        populate_sections(text, session)

    # Populate paragraphs and solutions
    populate_solutions_and_paragraphs(text)


def process_book(filepath: str) -> None:
    """
    Parse book from a file and save exercises, paragrapgs
    and sections to the database.
    Args:
        filepath (str): file path to the book in markdown extension
    """
    # Read the book
    with open(filepath, "r") as file:
        text = file.read()

    # Populate paragraphs and exercises
    populate_exercises(text)


def populate_database(bookpath: str, solutionpath: str) -> None:
    # Process solution mannual to populate sections, paragraphs and solutions tables
    process_solution_mannual(solutionpath)

    # Process book to populate exercises table
    process_book(bookpath)


if __name__ == "__main__":
    initialize_database()
    populate_database(config.BOOK_FILEPATH, config.SOLUTIONS_FILEPATH)
