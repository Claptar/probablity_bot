from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from app.database.models.solved_exercises import SolvedExercise
from app.telegram_bot.handlers.commands import challenge_command

async def handle_response(text: str) -> str:
    return text[::-1]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_response(update.message.text)
    await update.message.reply_text(response)
