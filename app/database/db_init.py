from app import config
from re import Match
from typing import Type
from app.database.models import Base, Exercise, Solution, engine
from app.database.utils import session_scope
from app.parsers import get_exercises


def process_paragraphs(filepath: str, model: Type[Base]) -> None:
    """
    Parse paragraphs from a file and save exercises to the database
    Args:
        filepath (str): file path to the book in markdown extension
    """
    # Read the book
    parsed_exercises = get_exercises(filepath)

    # Write exercises to the database
    with session_scope(engine) as session:
        for exercise_data in parsed_exercises:
            # Get exercise_id if we process a solution exercise
            if model is Solution:
                relative_exercise = Exercise.get_by_number_and_paragraph(
                    session,
                    exercise_data["number"],
                    exercise_data["paragraph"],
                )
                exercise_data.update(exercise_id=relative_exercise.id)
            # Finally write to the database
            exercise = model.create(session, exercise_data)


def main():
    Base.metadata.create_all(engine)
    process_paragraphs(config.BOOK_FILEPATH, Exercise)
    process_paragraphs(config.SOLUTIONS_FILEPATH, Solution)


if __name__ == "__main__":
    main()
