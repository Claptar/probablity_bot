from app.config import BOT_TOKEN
from app.telegram_bot import (
    help_command,
    challenge_command,
    start_command,
    score_command,
    leaderboard_command,
)
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from app.utils.logging_config import setup_logging


async def handle_response(text: str) -> str:
    return text[::-1]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_response(update.message.text)
    await update.message.reply_text(response)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    # set up logging
    setup_logging()

    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("challenge", challenge_command))
    application.add_handler(CommandHandler("score", score_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))

    # Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    application.add_error_handler(handle_error)

    # Run the bot
    application.run_polling(poll_interval=3)
