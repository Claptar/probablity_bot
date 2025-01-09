import re
from typing import Iterator

PARAGRAPH_PATTERN = re.compile(
    r"""
    \#+\s*                                      # One or more '#' followed by whitespace
    (?P<paragraph_num>[\dI][\.\s]*[\dI]*)       # Section number (captured)
    \s+                                         # Required whitespace
    (?P<title>.*?)                              # Section title (captured)
    \n+                                         # One or more newlines
    (?P<contents>.*?)                           # Main content (captured)
    (?:\n+\#\s*Exercises\n(?P<exercises>.*?))?  # Exercise section (captured)
    (?=\n\#\s*[\dI][\.\s]*[\dI]|$)              # Lookahead for next section or end
    """,
    re.VERBOSE | re.DOTALL | re.MULTILINE,
)

EXERCISE_PATTERN = re.compile(
    r"""
    (?P<exercise_num>\d+)       # Exercise number
    \.\s+                       # Required whitespace
    (?P<exercise_contents>.*?)  # Contenst of the exercise
    (?=\n\d+\.|\Z)              # Lookahead for next exercise or end
    """,
    re.VERBOSE | re.DOTALL,
)


def parse_paragraphs(text: str) -> Iterator[re.Match]:
    return PARAGRAPH_PATTERN.finditer(text)


def parse_exercises(text: str) -> Iterator[re.Match]:
    return EXERCISE_PATTERN.finditer(text)
