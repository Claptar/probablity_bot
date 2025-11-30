import re
from typing import Iterator

TITLE_PATTERN = re.compile(r"^#[\s\*]+(?P<number>\d{1,2}.\d{1,2})+(?P<title>.+)$")

ELEMENT_PATTERN = re.compile(
    r"""
    <<(?P<type>\w+)\s+(?P<number>[\d\.]+)>>
    (?P<content>.*?)
    <</(?P=type)\s+(?P=number)>>
    """,
    re.VERBOSE | re.DOTALL | re.MULTILINE,
)


def parse_title(text: str) -> re.Match:
    """
    Parse titles from a subsection text
    Args:
        text (str): subsection text
    Returns:
        re.Match: a regex match object for the title found, or None if no match
    """
    return TITLE_PATTERN.match(text)


def parse_elements(text: str) -> Iterator[re.Match]:
    """
    Parse elements from a subsection text
    Args:
        text (str): subsection text
    Returns:
        Iterator[re.Match]: an iterator over regex match objects for each element found
    """
    return ELEMENT_PATTERN.finditer(text)
