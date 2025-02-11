" Command handlers for the /challendge command "
import os
import logging
import tempfile
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from app.database.quieries.queries import get_random_exercise, update_users_exercise
from app.utils import latex_to_png


CHALLENGE_MESSAGE = "Here comes the trial\!⚡"


async def challenge_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Challenge command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # Notify user that you are generating an answer
    await update.message.reply_chat_action("typing")

    # Get a random exercise
    exercise_id, exercise_text, paragraph_title = get_random_exercise(
        first_name=update.effective_user.first_name,
        telegram_id=update.effective_user.id,
        username=update.effective_user.username,
    )

    # Update user's current exercise
    update_users_exercise(update.effective_user.id, exercise_id)

    # Render exercise image
    logging.info("Rendering LaTeX to PNG for exercise: %s", exercise_text)
    image_path = tempfile.mktemp(suffix=".png")
    latex_to_png(exercise_text, image_path)

    # Send the exercise to the user
    reply_keyboard = [["Next trial", "Give me the answer!"], ["Give me some rest"]]

    await update.message.reply_text(
        CHALLENGE_MESSAGE,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            input_field_placeholder="What is your answer?",
            resize_keyboard=True,
        ),
    )
    await update.message.reply_chat_action("upload_photo")
    await update.message.reply_photo(
        photo=image_path, caption=f"Section: {paragraph_title}"
    )

    # Remove the image
    os.remove(image_path)
    return "TRIAL"
