import re
from typing import Iterator, Dict

PARAGRAPH_PATTERN = re.compile(
    r"""
    \#+\s*                                      # One or more '#' followed by whitespace
    (?P<number>[\dI][\.\s]+[\dI])              # Section number (captured)
    \s+                                         # Required whitespace
    (?P<title>[\w\s]+)                              # Section title (captured)
    \n+                                         # One or more newlines
    (?P<contents>.*?)                           # Main content (captured)
    (?P<exercises>(?:\#+\s*Exercises\n.*?)?)  # Exercise section (captured)
    (?=\n\#+\s*[\dI][\.\s]+[\dI]|\Z)              # Lookahead for next section or end
    """,
    re.VERBOSE | re.DOTALL | re.MULTILINE,
)

EXERCISE_PATTERN = re.compile(
    r"""
    (?P<number>\d+)         # Exercise number
    \.\s+                       # Required whitespace
    (?P<contents>.*?)  # Contenst of the exercise
    (?=\n\d+\.|\Z)              # Lookahead for next exercise or end
    """,
    re.VERBOSE | re.DOTALL,
)


def parse_paragraphs(text: str) -> Iterator[re.Match]:
    return PARAGRAPH_PATTERN.finditer(text)


def get_paragraph_data(paragraph_match: re.Match) -> Dict[str, str]:
    return paragraph_match.groupdict()


def parse_exercises(text: str) -> Iterator[re.Match]:
    return EXERCISE_PATTERN.finditer(text)


def get_exercise_data(
    paragraph_match: re.Match, exercise_match: re.Match
) -> Dict[str, str]:
    paragraph = paragraph_match.group("number")
    return dict(paragraph=paragraph, **exercise_match.groupdict())
