" Select command handler "
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from app.database.quieries.queries import get_sections
from app.database.quieries.queries import get_selected_sections

SELECT_MESSAGE = "So, you want to choose thrials you are more confidant in\. Fine, here is a rough section categories of my trials\. Do you want me to make it more detailed?\n\n"


def format_title(title, section_id, selected_sections) -> str:
    """
    Get the status of the section
    Args:
        title (str): Section title
        id (int): Section id
        selected_sections (list): List of selected sections
    Returns:
        str: Status of the section
    """
    return f"{'✅' if section_id in selected_sections else '❌'} _{title}_"


async def select_command(update: Update, context: CallbackContext) -> str:
    """
    Select command handler
    Args:
        update (Update): Telegram update object
        context (CallbackContext): Telegram context object
    Returns:
        str: Conversation state
    """
    # Notify user that you are generating an answer
    await update.message.reply_chat_action("typing")

    # Get all sections
    sections = get_sections()

    # Get user's selected section
    selected_sections = get_selected_sections(update.effective_user.id)

    # Create a message with sections
    formated_sections = [
        format_title(title, section_id, selected_sections)
        for section_id, title in sections.items()
    ]
    message = SELECT_MESSAGE + "\n".join(formated_sections)

    # Create a keyboard with sections
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data="YES"),
            InlineKeyboardButton("No", callback_data="NO"),
        ],
        [
            InlineKeyboardButton("Cancel", callback_data="CANCEL"),
        ],
    ]

    # Send the sections to the user
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        message,
        parse_mode="MarkdownV2",
        reply_markup=reply_markup,
    )
    return "SELECT"
