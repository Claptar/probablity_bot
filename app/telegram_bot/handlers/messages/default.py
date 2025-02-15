" Handlers for the ordinary messages sent by the user. "
from telegram import Update
from telegram.ext import ContextTypes


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle incoming user messages by sending a typing action and a response text.

    Parameters:
        update (Update): The Telegram update object representing the incoming message.
        context (ContextTypes.DEFAULT_TYPE): The context object providing relevant data and
                                              helper methods for handling the update.
    """
    response = "Enough of your chit-chat... Return to the trial!🌀"
    await update.message.reply_chat_action("typing")
    await update.message.reply_text(response)
