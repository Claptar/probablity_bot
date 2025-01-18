import re
from typing import Iterator

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


def parse_paragraphs(text: str) -> Iterator[re.Match]:
    """
    Parse paragraphs from a book
    Args:
        text (str): book text in markdown format

    Returns:
        Iterator[re.Match]: iterator of paragraph matches
    """
    return PARAGRAPH_PATTERN.finditer(text)
