from models import Base, engine, Exercise
from re import Match
from parsers import parse_paragraphs, parse_exercises, get_exercise_data
import config


def process_paragraphs(filepath: str) -> None:
    """
    Parse paragraphs from a file and save exercises to the database
    Args:
        filepath (str): file path to the book in markdown extension
    """
    # Read the book
    with open(filepath, "r") as file:
        text = file.read()

    # Parse the book paragraph by paragraph and add exercises to the DataBase
    for paragraph_match in parse_paragraphs(text):
        # parse exercise section of the book
        exercise_section = paragraph_match.group("exercises") or ""
        for exercise_match in parse_exercises(exercise_section):
            exercise = get_exercise_data(paragraph_match, exercise_match)
            Exercise.save(exercise)


def main():
    Base.metadata.create_all(engine)
    process_paragraphs(config.BOOK_FILEPATH)


if __name__ == "__main__":
    main()
