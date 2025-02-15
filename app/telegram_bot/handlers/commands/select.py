" Select command handler "
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from app.database.quieries.queries import get_sections

SELECT_MESSAGE = "So, you want to choose thrials you are more confidant in\. Fine, here is a rough categorization of the trials\. Now choose!"


async def select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Select command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # Notify user that you are generating an answer
    await update.message.reply_chat_action("typing")

    # Get the sections
    sections = get_sections()

    # Create a keyboard with sections
    keyboard = [
        [InlineKeyboardButton(title, callback_data=id)]
        for id, title in sections.items()
    ]

    # Send the sections to the user
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        SELECT_MESSAGE,
        parse_mode="MarkdownV2",
        reply_markup=reply_markup,
    )
    return "SELECT"
