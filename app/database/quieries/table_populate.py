from sqlalchemy.orm import Session
from app.database.models import Exercise, Solution, Section, Paragraph


def add_paragraph(
    section_number: str, paragraph_data: str, session: Session
) -> Paragraph:
    """
    Create a paragraph and save it to the database.
    Args:
        section_number (str): section number
        paragraph_data (str): paragraph data
        session (Session): database session
    Returns:
        Paragraph: created paragraph
    """
    section = Section.section_by_number(section_number, session)
    paragraph = Paragraph(section_id=section.id, **paragraph_data)
    session.add(paragraph)
    return paragraph
