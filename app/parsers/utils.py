import re
from typing import Dict, Iterator
from app.parsers.paragraph import parse_paragraphs
from app.parsers.exercise import parse_exercises


def normalize_number(number: str) -> str:
    """
    Validates and normalizes the paragraph field by:
    - Removing spaces
    - Replacing 'I' with '1'
    - Replacing 'O' with '0'
    Args:
        number (str): paragraph number

    Returns:
        str: normalized paragraph number
    """
    return number.replace(" ", "").translate(str.maketrans({"I": "1", "O": "0"}))


def get_exercise_data(
    paragraph_match: re.Match, exercise_match: re.Match
) -> Dict[str, str]:
    """
    Convert paragraph and exercise match-groups to dict with exercise data
    Args:
        paragraph_match (re.Match): paragraph Match object
        exercise_match (re.Match): exercise Match object

    Returns:
        Dict[str, str]: exercise data dict
    """
    paragraph_number = paragraph_match.group("number")
    paragraph_number = normalize_number(paragraph_number)
    return dict(paragraph=paragraph_number, **exercise_match.groupdict())


def get_exercises(filepath: str) -> Iterator[re.Match]:
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
        # get exercise section of the book
        if "Exercises" in paragraph_match.group("title"):
            exercise_section = paragraph_match.group("contents")
        else:
            exercise_section = paragraph_match.group("exercises") or ""

        # parse exercises
        for exercise_match in parse_exercises(exercise_section):
            exercise = get_exercise_data(paragraph_match, exercise_match)
            yield exercise
