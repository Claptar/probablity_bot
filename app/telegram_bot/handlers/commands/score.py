" Command handler for the /score command "
from string import Template
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from app.database.quieries.queries import get_user_score

SCORE_MESSAGE = Template(
    "Let me see\.\. Hmm\.\. Through you challenges you have gained *$value points* of casuality\! 🌀🔢"
)


async def score_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Score command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # Notify user that you are generating an answer
    await update.message.reply_chat_action("typing")

    score = get_user_score(update.effective_user.id)
    formated_message = SCORE_MESSAGE.substitute(value=score)
    await update.message.reply_text(formated_message, parse_mode=ParseMode.MARKDOWN_V2)
