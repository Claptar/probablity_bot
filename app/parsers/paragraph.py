import re
from typing import Iterator, Dict, Tuple, Union
from app.paersers.utils import normalize_number

PARAGRAPH_PATTERN = re.compile(
    r"""
    ^\#+\s*[^I1]?\s*                                # One or more '#' followed by whitespace
    (?P<number>[\dIO]+[\.\s]+[\dIO]+)              # Section number (captured)
    \s+                                        # Required whitespace
    (?P<title>[\w '-]+)$                         # Section title (captured)
    (?P<contents>(?:.*?)?)                          # Main content (captured)
    ^(?P<exercises>(?:(?:\#+\s*Exercises|\#+\s*Solutions\sto\sExercises|^\d\.)\s*.*?)?)   # Exercise section (captured)
    (?=^\#+\s*[^I1]?\s*[\dIO]+[\.\s]+[\dIO]+|\Z)        # Lookahead for next section or end
    """,
    re.VERBOSE | re.DOTALL | re.MULTILINE,
)


def parse_paragraphs(text: str) -> Iterator[re.Match]:
    """
    Parse paragraphs from a book
    Args:
        text (str): book text in markdown format

    Returns:
        Iterator[re.Match]: iterator of paragraph matches
    """
    return PARAGRAPH_PATTERN.finditer(text)


def get_section_and_paragraph_numbers(paragraph_match: re.Match) -> Tuple[int, int]:
    """
    Split the full paragraph number into section and paragraph numbers
    Args:
        paragraph_match (re.Match): paragraph Match object

    Returns:
        Tuple[str, str]: section and paragraph numbers
    """
    full_number = paragraph_match.group("number")
    normalized_full_number = normalize_number(full_number)
    section_number, paragraph_number = normalized_full_number.split(".")
    return section_number, paragraph_number


def get_paragraph_data(paragraph_match: re.Match) -> Dict[str, str]:
    """
    Convert paragraph match-groups to dict with paragraph data
    Args:
        paragraph_match (re.Match): paragraph Match object

    Returns:
        Dict[str, str]: paragraph data dict
    """
    _, paragraph_number = get_section_and_paragraph_numbers(paragraph_match)

    # Make a dict with paragraph data
    paragraph_data = {
        "number": paragraph_number,
        "title": paragraph_match.group("title"),
        "contents": paragraph_match.group("contents"),
    }
    return paragraph_data


def get_paragraphs(text: str) -> Iterator[Tuple[int, str, Dict[str, str]]]:
    """
    Get paragraphs from a book text
    Args:
        text (str): book text in markdown format
    Yields:
        Iterator[Tuple[int, str, Dict[str, str]]]: section number, exercise section, and paragraph data
    """
    # Parse the book paragraph by paragraph
    for paragraph_match in parse_paragraphs(text):
        section_number, _ = get_section_and_paragraph_numbers(paragraph_match)
        paragraph_data = get_paragraph_data(paragraph_match)
        exercise_section = paragraph_match.group("exercises")
        yield section_number, exercise_section, paragraph_data
