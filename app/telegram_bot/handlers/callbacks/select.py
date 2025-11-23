" This module contains the callback function for the section selection. "
from string import Template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from telegram.ext import ContextTypes, ConversationHandler
from app.database.queries.table_populate import (
    add_selected_paragraph,
)
from app.database.queries.queries import (
    select_all_section_paragraphs,
    get_selected_sections,
    get_selected_section_paragraphs,
)
from app.telegram_bot.handlers.utils import get_paragraph_keyboard, get_section_keyboard

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

    if query.data == "DONE" or query.data == "CANCEL":
        return await _done_callback(query)
    elif query.data.isnumeric():
        return await _select_section(query, update.effective_user.id)
    elif query.data.replace("-", "").isnumeric():
        context.user_data["section_id"] = query.data.replace("-", "")
        return await _select_paragraphs(
            query, update.effective_user.id, context.user_data["section_id"]
        )
    else:
        return ValueError("Invalid callback data")


async def _select_section(query: CallbackQuery, user_id: str) -> str:
    """
    Callback function for the section selection
    Args:
        query (CallbackQuery): Telegram callback query object
        user_id (str): Telegram user id
    Returns:
        str: Conversation state
    """
    # Notify user that you are generating an answer
    await query.message.reply_chat_action("typing")

    # Get user's selected section
    selected_sections = get_selected_sections(user_id)

    # Check if the last query was for sections and select/unselect all paragraphs
    if query.data.isnumeric():
        section_id = int(query.data)
        select = selected_sections[section_id]["selected_count"] == 0
        select_all_section_paragraphs(user_id, query.data, select)
        selected_sections[section_id]["selected_count"] = (
            selected_sections[section_id]["paragraph_count"] if select else 0
        )

    # Create a keyboard
    keyboard = get_section_keyboard(selected_sections)

    # Add a cancel button
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


async def _select_paragraphs(
    query: CallbackQuery, user_id: str, section_id: str
) -> str:
    """
    Callback function for the section selection
    Args:
        query (CallbackQuery): Telegram callback query object
        user_id (str): Telegram user id
    Returns:
        str: Conversation state
    """
    if int(query.data) > 0:
        add_selected_paragraph(user_id, int(query.data))

    # Get user's selected paragraphs for the section
    selected_paragraphs = get_selected_section_paragraphs(user_id, section_id)

    # Create a keyboard with paragraphs
    keyboard = get_paragraph_keyboard(selected_paragraphs)
    keyboard.append(
        [
            InlineKeyboardButton("Back", callback_data="BACK"),
            InlineKeyboardButton("Done", callback_data="DONE"),
        ]
    )

    # Send the message to the user
    await query.edit_message_text(
        MESSAGE.substitute(value="paragraphs"),
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

    match query.data:
        case "DONE":
            return await _done_callback(query)
        case "BACK":
            return await _select_section(query, update.effective_user.id)
        case _:
            return await _select_paragraphs(
                query, update.effective_user.id, context.user_data["section_id"]
            )
