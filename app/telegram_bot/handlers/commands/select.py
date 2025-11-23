" Select command handler "
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from app.database.queries.queries import get_selected_sections
from app.telegram_bot.handlers.utils import get_section_keyboard

SELECT_MESSAGE = "So, you want to choose trials you are more confident in\. Fine, here is a rough categories of my trials\. Make your choice\!"


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

    # Get user's selected section
    selected_sections = get_selected_sections(update.effective_user.id)

    # Create a keyboard with sections
    keyboard = get_section_keyboard(selected_sections)

    # Add a cancel button
    keyboard.append([InlineKeyboardButton("Cancel", callback_data="CANCEL")])

    # Send the message to the user
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        SELECT_MESSAGE,
        parse_mode="MarkdownV2",
        reply_markup=reply_markup,
    )
    return "SECTION"
