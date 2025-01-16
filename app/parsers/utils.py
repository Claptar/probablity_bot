import re
from typing import Dict


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


def get_exercise_data(
    paragraph_match: re.Match, exercise_match: re.Match
) -> Dict[str, str]:
    """
    Convert paragraph and exercise match-groups to dict with exercise data
    Args:
        paragraph_match (re.Match): paragraph Match object
        exercise_match (re.Match): exercise Match object

    Returns:
        Dict[str, str]: exercise data dict
    """
    paragraph_number = paragraph_match.group("number")
    paragraph_number = normalize_number(paragraph_number)
    return dict(paragraph=paragraph_number, **exercise_match.groupdict())
