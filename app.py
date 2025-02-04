"Contains app's main logic"
from telegram import Update
from telegram.ext import (
    Application,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from app.utils.logging_config import setup_logging
from app.config import BOT_TOKEN
from app.telegram_bot.handlers.commands import (
    help_command,
    challenge_command,
    start_command,
    score_command,
    leaderboard_command,
    solution_command,
)

from app.telegram_bot.handlers.messages import handle_message, give_rest, solved


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    # set up logging
    setup_logging()

    application = Application.builder().token(BOT_TOKEN).build()

    # Cinversation handler
    challenge_command_handler = ConversationHandler(
        entry_points=[CommandHandler("challenge", challenge_command)],
        states={
            "TRIAL": [
                MessageHandler(
                    filters.Regex("^(Next trial)$"),
                    challenge_command,
                ),
                MessageHandler(
                    filters.Regex("^(Give me the answer!)$"),
                    solution_command,
                ),
                MessageHandler(
                    filters.Regex("^(Give me some rest)$"),
                    give_rest,
                ),
            ],
            "SOLUTION": [
                MessageHandler(
                    filters.Regex("^(Next trial)$"),
                    challenge_command,
                ),
                MessageHandler(
                    filters.Regex("^(Solved it!)$"),
                    solved,
                ),
                MessageHandler(
                    filters.Regex("^(Give me some rest)$"),
                    give_rest,
                ),
            ],
            "SOLVED": [
                MessageHandler(
                    filters.Regex("^(Next trial)$"),
                    challenge_command,
                ),
                MessageHandler(
                    filters.Regex("^(Give me some rest)$"),
                    give_rest,
                ),
            ],
        },
        fallbacks=[
            CommandHandler("help", help_command),
            CommandHandler("score", score_command),
            CommandHandler("leaderboard", leaderboard_command),
            CommandHandler("solution", solution_command),
            MessageHandler(filters.TEXT, handle_message),
        ],
    )

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("score", score_command))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CommandHandler("solution", solution_command))
    application.add_handler(challenge_command_handler)

    # Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    application.add_error_handler(handle_error)

    # Run the bot
    application.run_polling(poll_interval=3)
