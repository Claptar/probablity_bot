import re
from typing import Iterator, Dict, Tuple
from app.parsers.utils import normalise_number

SUBSECTION_PATTERN = re.compile(
    r"""
    ^\#+\s*[^I1]?\s*                                # One or more '#' followed by whitespace
    (?P<number>[\dIO]+[\.\s]+[\dIO]+)              # subsection number (captured)
    \s+                                        # Required whitespace
    (?P<title>[\w '-]+)$                         # subsection title (captured)
    (?P<contents>(?:.*?)?)                          # Main content (captured)
    (?P<exercises>(?:(?:^\#+\s*Exercises|^\#+\s*Solutions\sto\sExercises|(?<![\.\:\$]\n\n)(?<![\.\:\$]\n)^\d\.)\s*.*?)?)   # Exercise section (captured)
    (?=^\#+\s*[^I1]?\s*[\dIO]+[\.\s]+[\dIO]+|\Z)        # Lookahead for next section or end
    """,
    re.VERBOSE | re.DOTALL | re.MULTILINE,
)


def match_subsections(text: str) -> Iterator[re.Match]:
    """
    Parse subsections from a book
    Args:
        text (str): book text in markdown format

    Returns:
        Iterator[re.Match]: iterator of subsection matches
    """
    return SUBSECTION_PATTERN.finditer(text)


def get_subsection_data(subsection_match: re.Match) -> Dict[str, str]:
    """
    Convert subsection match-groups to dict with subsection data
    Args:
        subsection_match (re.Match): subsection Match object

    Returns:
        Dict[str, str]: subsection data dict
    """
    # Get section and subsection numbers
    full_number = subsection_match.group("number")
    normalized_full_number = normalise_number(full_number)
    section_number, subsection_number = normalized_full_number.split(".")

    # Make a dict with subsection data
    subsection_data = {
        "section": section_number,
        "number": subsection_number,
        "title": subsection_match.group("title"),
        "contents": subsection_match.group("contents"),
        "exercises": subsection_match.group("exercises"),
    }
    return subsection_data
