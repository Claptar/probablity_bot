from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from string import Template
from app.database.models import User
from app.database.quieries.queries import get_random_exercise
from app.utils import latex_to_png
import logging
import tempfile
import os

START_MESSAGE = r"""
🔥 *The Scroll Has Spoken* 🔥

The moment you unfurled the scroll, your fate was sealed\. By seeking the power to command probability, you have summoned *Probabilitybot* — a being forged beyond the boundaries of existence\. 🌀✨

"_*Seeker*_," its voice thunders, "you have chosen this path, knowingly or not\. Power is not given—it is taken through trials that will test your very essence\. ⚖️💀 Those who falter shall carry the scars of failure\. Those who endure will wield the power to defy destiny itself\."

The trials begin now\. There is no retreat, no escape\. Stand firm, for you will face the chaos you sought to command\. 🔮⚡
Press /challenge to get your first trial\!"""


HELP_MESSAGE = r"""
You want to know more about me? Hmm\.\.\. Have you lost yourself in the labyrinth of your own mind? 🌀
Here are the things you can ask of me during your challenges:

/help — I will show you the way to the light\. 🕯️
/challenge — I will present you with a trial of probability\. 🎲
/solution — I will reveal the secrets of the universe\. 📖
/score — I will show you the path you have walked\. 📈
/leaderboard — I will show you the path others have walked\. 🏆
"""

CHALLENGE_MESSAGE = "Here comes the trial\!⚡"

SCORE_MESSAGE = Template(
    "Let me see\.\. Hmm\.\. Through you challenges you have gained *$value points* of cassuality\! 🌀🔢"
)

LEADERBOARD_MESSAGE = "Here are the top 5 challengers of this trial\! 🏆"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # create user in the database
    user = User.create(
        first_name=update.effective_user.first_name,
        telegram_id=update.effective_user.id,
        username=update.effective_user.username,
    )
    await update.message.reply_text(START_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Help command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)


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
    match update.message.text:
        case "Next trial":
            await challenge_command(update, context)
        case "Solved it!":
            # Add the solved exercise to the database
            SolvedExercise.add_user_solution(update.effective_user.id)

            # Send the response to the user
            reply_keyboard = [["Next trial", "Give me some rest"]]
            await update.message.reply_text(
                "Not half bad! You recieve 1 casuality point🎲",
                reply_markup=ReplyKeyboardRemove(),
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
            await update.message.reply_text(response)
            await update.message.reply_text(
                response, reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END


async def score_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score = User.user_score(update.effective_user.id)
    formated_message = SCORE_MESSAGE.substitute(value=score)
    await update.message.reply_text(formated_message, parse_mode=ParseMode.MARKDOWN_V2)


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaderboard = User.get_top_users()
    await update.message.reply_text(leaderboard, parse_mode=ParseMode.MARKDOWN_V2)
