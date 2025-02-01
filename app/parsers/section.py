import re
from typing import Iterator


SECTION_PATTERN = re.compile(
    r"""
    ^\#\#\s+Chapter\s(?P<number>\d{1,2})$   # Section number
    \n+                                     # Required empty lines
    ^\#\#\s+(?P<title>[\w ]+)$              # Section title
    """,
    re.VERBOSE | re.MULTILINE,
)


def parse_sections(text: str) -> Iterator[re.Match]:
    """
    Parse sections from a solution mannual
    Args:
        text (str): solution mannual's text in markdown format

    Returns:
        Iterator[re.Match]: iterator of section matches
    """
    return SECTION_PATTERN.finditer(text)
