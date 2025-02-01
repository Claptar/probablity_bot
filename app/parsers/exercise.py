import re
from typing import Iterator, Tuple, Dict
from app.parsers.paragraph import get_paragraphs


EXERCISE_PATTERN = re.compile(
    r"""
    ^\#*\s*(?P<number>\d+)         # Exercise number
    \.\s+                   # Required whitespace
    (?P<contents>.*?)       # Contenst of the exercise
    (?=^\#*\s*\d+\.|\Z)            # Lookahead for next exercise or end
    """,
    re.VERBOSE | re.DOTALL | re.MULTILINE,
)


def parse_exercises(text: str) -> Iterator[re.Match]:
    """
    Parse exercises from a exercise section of a book
    Args:
        text (str): exercise section text

    Returns:
        Iterator[re.Match]: iterator of exercise matches
    """
    return EXERCISE_PATTERN.finditer(text)


def get_exercises(text: str) -> Iterator[Tuple[str, Dict[str, str]]]:
    """
    Get paragraphs from a book text
    Args:
        text (str): book text in markdown format

    Yields:
    """
    for section_number, exercise_section, paragraph_data in get_paragraphs(text):
        exercise = parse_exercises(exercise_section)
        for exercise_match in exercise:
            yield section_number, paragraph_data["number"], exercise_match.groupdict()
