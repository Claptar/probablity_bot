"Contains app's main logic"
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from app.utils.logging_config import setup_logging
from app.config import BOT_TOKEN
from app.telegram_bot.handlers.commands import (
    help_command,
    start_command,
    score_command,
    leaderboard_command,
    solution_command,
)

from app.telegram_bot.handlers.messages import handle_message
from app.telegram_bot.handlers.conversations import (
    challenge_conversation_handler,
    select_conversation_handler,
)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle errors
    Args:
        update (Update): Update object
        context (ContextTypes.DEFAULT_TYPE): Context object
    """
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    # set up logging
    setup_logging()

    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("score", score_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CommandHandler("solution", solution_command))

    # Conversation handlers
    application.add_handler(challenge_conversation_handler)
    application.add_handler(select_conversation_handler)

    # Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    application.add_error_handler(handle_error)

    # Run the bot
    application.run_polling(poll_interval=3)
