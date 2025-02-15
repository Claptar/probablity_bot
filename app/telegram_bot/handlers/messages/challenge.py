" Handlers for the messages sent by the user. "
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from app.database.quieries.table_populate import add_solved_exercise

async def solved(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the solved command by logging the event, updating the database with the user's solution, and sending appropriate responses to the user.
    Parameters:
        update (Update): The incoming update containing user and message details.
        context (ContextTypes.DEFAULT_TYPE): The context containing additional data and methods for the current update.
    Returns:
        str: A state identifier ("SOLVED") used to guide the conversation flow.
    """
    # Add the solved exercise to the database
    logging.info("User %s solved the exercise", update.effective_user.id)
    add_solved_exercise(update.effective_user.id)

    # Send the response to the user
    reply_keyboard = [["Next trial", "Give me some rest"]]

    await update.message.reply_chat_action("typing")
    await update.message.reply_text("Not half bad! You receive 1 casuality point🎲")

    await update.message.reply_chat_action("typing")
    await update.message.reply_text(
        "Another trial awaits you🌀",
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            input_field_placeholder="State your answer",
            resize_keyboard=True,
        ),
    )
    return "SOLVED"


async def give_rest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the user's request to finish the current challenge and restore their energy.

    Parameters:
        update (Update): The update object that contains information about the incoming update.
        context (ContextTypes.DEFAULT_TYPE): The context object that holds additional data
            relevant to the current update and conversation.

    Returns:
        int: ConversationHandler.END to signal the termination of the conversation.
    """
    logging.info("User %s requested to finish challendge", update.effective_user.id)
    response = "Hmm.. Seems like you need to restore your energy. Fine...🌌"
    await update.message.reply_chat_action("typing")
    await update.message.reply_text(response, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END