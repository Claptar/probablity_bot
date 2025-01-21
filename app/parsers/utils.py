import re
from typing import Dict, Iterator
from app.parsers.paragraph import parse_paragraphs
from app.parsers.exercise import parse_exercises


def normalize_number(number: str) -> str:
    """
    Validates and normalizes the paragraph field by:
    - Removing spaces
    - Replacing 'I' with '1'
    - Replacing 'O' with '0'
    Args:
        number (str): paragraph number

    Returns:
        str: normalized paragraph number
    """
    return number.replace(" ", "").translate(str.maketrans({"I": "1", "O": "0"}))
