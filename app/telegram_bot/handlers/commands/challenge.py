" Command handlers for the /challendge command "
import os
import logging
import tempfile
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode
from app.database.models import User, SolvedExercise
from app.database.quieries.queries import get_random_exercise
from app.utils import latex_to_png


CHALLENGE_MESSAGE = "Here comes the trial\!⚡"


async def challenge_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Challenge command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # Get a random exercise
    exercise_id, exercise_text, exercise_title = get_random_exercise(
        first_name=update.effective_user.first_name,
        telegram_id=update.effective_user.id,
        username=update.effective_user.username,
    )

    # Update user's current exercise
    User.update_exercise(update.effective_user.id, exercise_id)

    # Render exercise image
    logging.info(f"Rendering LaTeX to PNG for exercise: {exercise_id}")
    image_path = tempfile.mktemp(suffix=".png")
    latex_to_png(exercise_text, image_path)

    # Send the exercise to the user
    reply_keyboard = [["Next trial", "Solved it!"], ["Give me some rest"]]

    await update.message.reply_text(
        CHALLENGE_MESSAGE,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            input_field_placeholder="What is your answer?",
            resize_keyboard=True,
        ),
    )
    await update.message.reply_photo(
        photo=image_path, caption=f"Section: {exercise_title}"
    )

    # Remove the image
    os.remove(image_path)
    return "TRIAL"


async def challenge_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    This function handles the response from the user after /challengde command
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object

    Returns:
        _type_: _description_
    """
    match update.message.text:
        case "Next trial":
            await challenge_command(update, context)
        case "Solved it!":
            # Add the solved exercise to the database
            SolvedExercise.add_user_solution(update.effective_user.id)

            # Send the response to the user
            reply_keyboard = [["Next trial", "Give me some rest"]]
            await update.message.reply_text(
                "Not half bad! You recieve 1 casuality point🎲"
            )
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
        case "Give me some rest":
            response = "Hmm.. Seems like you need to restore your energy. Fine...🌌"
            await update.message.reply_text(
                response, reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END
