" Command handler for the /leaderboard command "
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from app.database.models import User


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Leaderboard command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # Notify user that you are generating an answer
    await update.message.reply_chat_action("typing")

    leaderboard = User.get_top_users()
    await update.message.reply_chat_action("typing")
    await update.message.reply_text(leaderboard, parse_mode=ParseMode.MARKDOWN_V2)
