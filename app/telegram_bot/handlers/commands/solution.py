" Command handlers for the /soluition command "
import os
import logging
import tempfile
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from app.database.quieries.queries import user_exercise_soluiton
from app.utils import latex_to_png


SOLUTION_MESSAGE = "You want to grasp the mystery of the universe? Fine\.\. 🌌"


async def solution_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Help command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # Notify user that you are generating an answer
    await update.message.reply_chat_action("typing")

    # Get the solution of the last exercise that the user tried
    solution_text = user_exercise_soluiton(update.effective_user.id)

    # Render exercise image
    logging.info("Rendering LaTeX to PNG for solution: %s", solution_text)
    image_path = tempfile.mktemp(suffix=".png")
    latex_to_png(solution_text, image_path)

    # Send the exercise to the user
    reply_keyboard = [["Next trial", "Solved it!"], ["Give me some rest"]]

    await update.message.reply_text(
        SOLUTION_MESSAGE,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            input_field_placeholder="What is your answer?",
            resize_keyboard=True,
        ),
    )
    await update.message.reply_chat_action("upload_photo")
    await update.message.reply_photo(photo=image_path)

    # Remove the image
    os.remove(image_path)
    return "SOLUTION"
