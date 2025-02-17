" Command handlers for the /soluition command "
import os
import logging
import tempfile
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from sqlalchemy.exc import NoResultFound
from app.database.quieries.queries import user_exercise_soluiton
from app.utils import latex_to_png


SOLUTION_MESSAGE = "You want to grasp the mystery of the universe? Fine\.\. 🌌"


async def solution_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str | None:
    """
    Help command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # Notify user that you are generating an answer
    await update.message.reply_chat_action("typing")

    # Get the solution of the last exercise that the user tried
    try:
        solution_text, exercise_id = user_exercise_soluiton(update.effective_user.id)
        return await send_solution(update, solution_text, exercise_id)
    except NoResultFound as e:
        logging.error("Error while getting the solution of the last exercise: %s", e)
        message = (
            "To grasp the mystery you have to go through a trial. Take the /challenge"
        )
        await update.message.reply_text(message)
    except Exception as e:
        logging.error(
            "Error while getting the solution exercise %s: %s", exercise_id, e
        )
        reply_keyboard = [["Next trial", "Give me some rest"]]
        message = f"I'm unable to grasp the solution for #trial{exercise_id} at the moment. Try again later."
        await update.message.reply_text(
            message,
            reply_markup=(
                ReplyKeyboardMarkup(
                    reply_keyboard,
                    input_field_placeholder="State your answer",
                    resize_keyboard=True,
                )
                if not update.message.entities
                else None
            ),
        )
        return "SOLVED"


async def send_solution(update, solution_text, exercise_id) -> str:
    """
    Send the solution to the user
    Args:
        update (Update): Telegram update object
        solution_text (str): The solution text
        exercise_id (int): The exercise ID
    Returns:
        str: The state identifier ("SOLUTION") used to guide the conversation flow
    """
    solution_text, exercise_id = user_exercise_soluiton(update.effective_user.id)

    # Render exercise image
    logging.info("Rendering LaTeX to PNG for solution: %s", solution_text)
    image_path = tempfile.mktemp(suffix=".png")
    latex_to_png(solution_text, image_path)

    # Send the exercise to the user
    reply_keyboard = [["Next trial", "Solved it!"], ["Give me some rest"]]

    await update.message.reply_text(
        SOLUTION_MESSAGE,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=(
            ReplyKeyboardMarkup(
                reply_keyboard,
                input_field_placeholder="What is your answer?",
                resize_keyboard=True,
            )
            if not update.message.entities
            else None
        ),
    )
    await update.message.reply_chat_action("upload_photo")
    await update.message.reply_photo(
        photo=image_path, caption=f"#solution #trial{exercise_id}"
    )

    # Remove the image
    os.remove(image_path)
    return "SOLUTION"
