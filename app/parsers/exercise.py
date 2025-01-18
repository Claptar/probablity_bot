import re
from typing import Iterator


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
