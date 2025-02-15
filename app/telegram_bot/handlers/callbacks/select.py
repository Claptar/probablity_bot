" This module contains the callback function for the section selection. "
from string import Template
from typing import List, Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import ContextTypes, ConversationHandler
from app.database.quieries.table_populate import (
    add_selected_section,
    add_selected_paragraph,
)
from app.database.quieries.queries import (
    get_sections,
    get_selected_sections,
    get_section_paragraphs,
    get_selected_section_paragraphs,
)

MESSAGE = Template("Here is a list of $value\. Choose carefully\.")


async def _done_callback(query: CallbackQuery) -> int:
    """
    Callback function for the done button
    Args:
        query (CallbackQuery): Telegram callback query object

    Returns:
        str: Conversation state
    """
    await query.edit_message_text("You've made you choice. Now return to the trials")
    return ConversationHandler.END


def _section_format(
    title: str, section_id: int, selected_sections: List[int], formating: bool = True
) -> str:
    """
    Get the status of the section
    Args:
        title (str): Section title
        id (int): Section id
        selected_sections (List[int]): List of selected sections
        format (bool): Format the title
    Returns:
        str: Status of the section
    """
    if formating:
        return f"{'✅' if section_id in selected_sections else '❌'} {title}\n"
    return f"{title}\n"


def _get_keyboard(
    sections: List[Dict[int, str]], selected_sections: List[int], formating: bool = True
) -> List[List[InlineKeyboardButton]]:
    """
    Get the keyboard with sections
    Args:
        sections (List[Dict[int, str]]): Dictionary with sections
        selected_sections (List[int]): List of selected sections
        format (bool): Format the title
    Returns:
        List[List[InlineKeyboardButton]]: Keyboard with sections
    """
    keyboard = [
        [
            InlineKeyboardButton(
                text=_section_format(title, section_id, selected_sections, formating),
                callback_data=section_id,
            )
        ]
        for section_id, title in sections.items()
    ]
    return keyboard


async def select_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Select callback function
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object

    Returns:
        str: Conversation state
    """
    # Notify user that you are generating an answer
    query = update.callback_query
    await query.answer()
    await query.message.reply_chat_action("typing")

    # Check if the user is done
    match query.data:
        case "NO":
            return await _select_section(query, update.effective_user.id)
        case "YES":
            return await _select_paragraph_section(query, update.effective_user.id)
        case "CANCEL":
            return await _done_callback(query)


async def section_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Callback function for the section selection
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    Returns:
        str: Conversation state
    """
    # Notify user that you are generating an answer
    query = update.callback_query
    await query.answer()
    await query.message.reply_chat_action("typing")

    match query.data:
        case "DONE":
            return await _done_callback(query)
        case _:
            return await _select_section(query, update.effective_user.id)


async def _select_section(query: CallbackQuery, user_id: str) -> str:
    """
    Callback function for the section selection
    Args:
        query (CallbackQuery): Telegram callback query object
        user_id (str): Telegram user id
    Returns:
        str: Conversation state
    """
    # Get sections
    sections = get_sections()

    # Check if the last query was for sections
    if query.data in map(str, sections.keys()):
        add_selected_section(user_id, int(query.data))

    # Get user's selected section
    selected_sections = get_selected_sections(user_id)

    # Create a message and keyboard with sections
    keyboard = _get_keyboard(sections, selected_sections)
    keyboard.append(
        [
            InlineKeyboardButton("Done", callback_data="DONE"),
        ]
    )

    # Send the sections to the user
    await query.edit_message_text(
        MESSAGE.substitute(value="sections"),
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return "SECTION"


async def _select_paragraph_section(query: CallbackQuery, user_id: str) -> str:
    """
    Callback function for the section selection
    Args:
        query (CallbackQuery): Telegram callback query object
        user_id (str): Telegram user id
    Returns:
        str: Conversation state
    """
    # Get sections
    sections = get_sections()

    # Get user's selected section
    selected_sections = get_selected_sections(user_id)

    # Create a message and keyboard with sections
    keyboard = _get_keyboard(sections, selected_sections, formating=False)
    keyboard.append(
        [
            InlineKeyboardButton("Cancel", callback_data="CANCEL"),
        ]
    )

    # Send the sections to the user
    await query.edit_message_text(
        MESSAGE.substitute(value="sections"),
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return "PARAGRAPH"


async def paragraph_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Callback function for the section selection
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    Returns:
        str: Conversation state
    """
    # Notify user that you are generating an answer
    query = update.callback_query
    await query.answer()
    await query.message.reply_chat_action("typing")

    # Set paragraph_id
    paragraph_id = query.data
    section_id = context.user_data.get("section_id", None)

    # Set section_id
    if section_id is None:
        paragraph_id = None
        section_id = query.data
        context.user_data["section_id"] = query.data

    match query.data:
        case "DONE":
            return await _done_callback(query)
        case "CANCEL":
            return await _done_callback(query)
        case "BACK":
            del context.user_data["section_id"]
            return await _select_paragraph_section(query, update.effective_user.id)
        case _:
            return await _select_paragraph(
                query, update.effective_user.id, section_id, paragraph_id
            )


async def _select_paragraph(
    query: CallbackQuery, user_id: str, section_id: str, paragraph_id: str
) -> str:
    """
    Callback function for the paragraph selection
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
        section_id (str): Section id
        paragraph_id (str): Paragraph id
    Returns:
        str: Conversation state
    """
    # Get all paragraphs for the section
    paragraphs = get_section_paragraphs(section_id)

    # Check if the last query was for paragraphs
    if paragraph_id in map(str, paragraphs.keys()):
        add_selected_paragraph(user_id, int(paragraph_id))

    # Get user's selected paragraphs for the section
    selected_paragraphs = get_selected_section_paragraphs(user_id, section_id)

    # Create a message and keyboard with sections
    keyboard = _get_keyboard(paragraphs, selected_paragraphs)
    keyboard.append(
        [
            InlineKeyboardButton("Back", callback_data="BACK"),
            InlineKeyboardButton("Done", callback_data="DONE"),
        ]
    )

    # Send the sections to the user
    await query.edit_message_text(
        MESSAGE.substitute(value="paragraphs"),
        parse_mode="MarkdownV2",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return "PARAGRAPH"
