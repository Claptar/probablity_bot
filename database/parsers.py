import re
from typing import Iterator, Dict

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


def get_paragraph_data(paragraph_match: re.Match) -> Dict[str, str]:
    return paragraph_match.groupdict()


def parse_exercises(text: str) -> Iterator[re.Match]:
    return EXERCISE_PATTERN.finditer(text)


def get_exercise_data(
    paragraph_match: re.Match, exercise_match: re.Match
) -> Dict[str, str]:
    paragraph = paragraph_match.group("number")
    return dict(paragraph=paragraph, **exercise_match.groupdict())
