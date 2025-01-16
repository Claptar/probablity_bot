import re
from typing import Iterator
from app.parsers.utils import get_exercise_data

PARAGRAPH_PATTERN = re.compile(
    r"""
    ^\#+\s*[^I1]?\s*                                # One or more '#' followed by whitespace
    (?P<number>[\dIO]+[\.\s]+[\dIO]+)              # Section number (captured)
    \s+                                        # Required whitespace
    (?P<title>[\w\s'-]+)$                         # Section title (captured)
    (?P<contents>.*?)                          # Main content (captured)
    (?P<exercises>(?:\#+\s*(?:Exercises|Solutions\sto\sExercises)\s*.*?)?)   # Exercise section (captured)
    (?=^\#+\s*[^I1]?\s*[\dIO]+[\.\s]+[\dIO]+|\Z)        # Lookahead for next section or end
    """,
    re.VERBOSE | re.DOTALL | re.MULTILINE,
)

EXERCISE_PATTERN = re.compile(
    r"""
    ^\#*\s*(?P<number>\d+)         # Exercise number
    \.\s+                   # Required whitespace
    (?P<contents>.*?)       # Contenst of the exercise
    (?=^\#*\s*\d+\.|\Z)            # Lookahead for next exercise or end
    """,
    re.VERBOSE | re.DOTALL | re.MULTILINE,
)


def parse_paragraphs(text: str) -> Iterator[re.Match]:
    return PARAGRAPH_PATTERN.finditer(text)


def parse_exercises(text: str) -> Iterator[re.Match]:
    """
    Parse exercises from a exercise section of a book
    Args:
        text (str): exercise section text

    Returns:
        _type_: Iterator[re.Match]

    Yields:
        Iterator[re.Match]: _description_
    """
    return EXERCISE_PATTERN.finditer(text)


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
