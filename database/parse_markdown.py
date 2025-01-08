import re
from re import Match
from typing import Iterator, Tuple, List


def get_paragraphs_iter(text: str) -> Iterator[Match]:
    """
    Parses the book in Markdown format with RegExo and creates an itterator over paragraphs in the book

    Args:
        text (str): book contents in the Markdown format

    Returns:
        Iterator[Match]: iterator containing all section matches
    """
    # Patterns for each group
    number_pattern = r"(?P<paragraph_num>[\dI][\.\s]+[\dI])"
    title_pattern = r"(?P<title>[\w\s]+)"
    contents_pattern = r"(?P<contents>.*?)"
    exercise_pattern = r"(?P<exercises>(?:\#+\s*Exercises\n.*?)?)"
    next_paragraph_pattern = r"(?=\n\#+\s*[\dI][\.\s]+[\dI]|\Z)"

    # Combine components into full pattern
    pattern = re.compile(
        rf"""
        \#+\s*                   # One or more '#' followed by whitespace
        {number_pattern}         # Section number (captured)
        \s+                      # Required whitespace
        {title_pattern}          # Section title (captured)
        \n+                      # One or more newlines
        {contents_pattern}       # Main content (captured)
        {exercise_pattern}       # Exercise section (captured)
        {next_paragraph_pattern} # Lookahead for next section or end
        """,
        re.VERBOSE | re.DOTALL,
    )

    # match patterns over the text
    matches = pattern.finditer(text, re.DOTALL)
    return matches


def get_exercises(text: str) -> Iterator[Match]:
    """
    Parse exercise section to get all exercises
    Args:
        text (str): exercise section contents

    Returns:
        Iterator[Match]: iterator containing all exercise matches
    """
    # Patterns for each group
    number_pattern = r"(?P<exercise_num>\d+)"
    contents_pattern = r"(?P<exercise_contents>.*?)"
    next_exercise = r"(?=\n\d+\.|\Z)"

    # Combine components into full pattern
    exercise_pattern = re.compile(
        rf"""
        {number_pattern}    # Exercise number
        \.\s+               # Required whitespace
        {contents_pattern}  # Contenst of the exercise
        {next_exercise}     # Lookahead for next exercise or end
        """,
        re.VERBOSE | re.DOTALL,
    )
    matches = exercise_pattern.finditer(text)
    return matches


if __name__ == "__main__":
    with open("example.md", "r") as f:
        sample_text = f.read()

    matches = get_paragraphs_iter(sample_text)
    first = next(matches)
    print("===================================")
    print(first.group("paragraph_num"))
    print("===================================")
    print(first.group("title"))
    print("===================================")
    print(first.group("contents"))
    print("===================================")
    print(first.group("exercises"))

    first = next(matches)
    print("===================================")
    print(first.group("paragraph_num"))
    print("===================================")
    print(first.group("title"))
    print("===================================")
    print(first.group("contents"))
    print("===================================")
    print(first.group("exercises"))

    exercise_matches = get_exercises(first.group("exercises"))
    for exercise in exercise_matches:
        print(exercise.group("exercise_num") + exercise.group("exercise_contents"))
        print("===================================")
