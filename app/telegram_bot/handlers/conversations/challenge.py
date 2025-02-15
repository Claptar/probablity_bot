" This module contains the conversation handler for the challenge command. "
from telegram import Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)
from app.telegram_bot.handlers.commands import (
    help_command,
    challenge_command,
    score_command,
    leaderboard_command,
    solution_command,
)
from app.telegram_bot.handlers.messages import handle_message, give_rest, solved

challenge_conversation_handler = ConversationHandler(
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
