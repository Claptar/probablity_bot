" This module contains the conversation handler for the select command. "
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from app.telegram_bot.handlers.commands import (
    help_command,
    score_command,
    leaderboard_command,
    select_command,
)
from app.telegram_bot.handlers.messages import handle_message
from app.telegram_bot.handlers.callbacks import (
    section_callback,
    paragraph_callback,
    select_callback,
)

select_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("select", select_command)],
    states={
        "SELECT": [
            CallbackQueryHandler(select_callback),
        ],
        "SECTION": [CallbackQueryHandler(section_callback)],
        "PARAGRAPH": [CallbackQueryHandler(paragraph_callback)],
    },
    fallbacks=[
        CommandHandler("help", help_command),
        CommandHandler("score", score_command),
        CommandHandler("leaderboard", leaderboard_command),
        MessageHandler(filters.TEXT, handle_message),
    ],
)
