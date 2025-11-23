" Command to remove the last solved exercise. "
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from sqlalchemy.exc import NoResultFound
from app.database.queries.queries import remove_last_solved_exercise


async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """
    Parameters:
        update (Update): The incoming update containing user and message details.
        context (ContextTypes.DEFAULT_TYPE): The context containing additional data and methods for the current update.
    Returns:
        str: ConversationHandler.END to signal the termination of the conversation.
    """
    logging.info(
        "User %s requested to remove the current challenge", update.effective_user.id
    )
    try:
        exercise_id = remove_last_solved_exercise(update.effective_user.id)
        message = f"You think that was just a luck? Okay, try again! I take back the casuality for #trial{exercise_id}"
        reply_keyboard = [["Next trial", "Give me some rest"]]
        await update.message.reply_text(
            message,
            reply_markup=(
                ReplyKeyboardMarkup(
                    reply_keyboard,
                    resize_keyboard=True,
                )
                if not update.message.entities
                else None
            ),
        )
        return "SOLVED"
    except NoResultFound as e:
        logging.error("Error while removing the last solved exercise: %s", e)
        message = (
            "What is there for me to take back? You haven't overcome any trials yet."
        )
        reply_keyboard = [["Next trial", "Give me some rest"]]
        await update.message.reply_text(
            message,
            reply_markup=(
                ReplyKeyboardMarkup(
                    reply_keyboard,
                    resize_keyboard=True,
                )
                if not update.message.entities
                else None
            ),
        )
        return "SOLVED"
