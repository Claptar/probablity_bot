from app.config import BOT_TOKEN
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I am a bot that can help you with your probability exercises."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I am a Probability Bot. Please look at commands I know: Command1, Command2, Command3"
    )


async def lolkek_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Lolkek")


async def handle_response(text: str) -> str:
    return text[::-1]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await handle_response(update.message.text)
    await update.message.reply_text(response)


async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lolkek", lolkek_command))

    # Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    application.add_error_handler(handle_error)

    # Run the bot
    application.run_polling(poll_interval=3)
