" Utils for handlers "
from typing import List, Dict, Any, Callable
from telegram import InlineKeyboardButton


def _format_paragraph_title(title: str, selected: bool) -> str:
    """
    Get the status of the section
    Args:
        title (str): Item's title
        select (bool): Is the item selected
    Returns:
        str: Status of the section
    """
    return f"{'✅' if selected else '❌'} {title}"


def _format_paragraph_number(section: List[Dict[int, Any]]) -> str:
    return f"{section['selected_count']}/{section['paragraph_count']} {'✅' if section['selected_count'] > 0 else '❌'}"


def get_paragraph_keyboard(
    paragraphs: List[Dict[int, Any]]
) -> List[List[InlineKeyboardButton]]:
    """
    Get the keyboard with sections
    Args:
        paragraphs (List[Dict[int, str]]): Dictionary with paragraphs
    Returns:
        List[List[InlineKeyboardButton]]: Keyboard with paragraphs
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text=_format_paragraph_title(paragraph["title"], paragraph["selected"]),
                callback_data=paragraph_id,
            )
        ]
        for paragraph_id, paragraph in paragraphs.items()
    ]
    return keyboard


def get_section_keyboard(
    sections: List[Dict[int, Any]]
) -> List[List[InlineKeyboardButton]]:
    """
    Get the keyboard with sections
    Args:
        sections (List[Dict[int, str]]): Dictionary with sections
    Returns:
        List[List[InlineKeyboardButton]]: Keyboard with sections
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text=section["title"],
                callback_data=section_id,
            ),
            InlineKeyboardButton(
                text=_format_paragraph_number(section),
                callback_data=-section["id"],
            ),
        ]
        for section_id, section in sections.items()
    ]
    return keyboard
