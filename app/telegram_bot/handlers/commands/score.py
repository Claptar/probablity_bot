" Command handler for the /score command "
from string import Template
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from app.database.queries.queries import get_user_score, count_solved_exercises

SCORE_MESSAGE = Template(
    "Let me see\.\. Hmm\.\. Through you challenges you have gained *$value points* of casuality\! 🌀🔢\n\n __*Number of solved trials by category:*__\n$table"
)


async def score_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Score command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # Notify user that you are generating an answer
    await update.message.reply_chat_action("typing")

    # get user's score
    score = get_user_score(update.effective_user.id)

    # get number of solved exercises
    solved_exercises_by_section = count_solved_exercises(update.effective_user.id)

    # Create a message
    table_list = [
        f"🔸{section['title']}: *{section['solved']}/{section['total']}*"
        for section in solved_exercises_by_section
    ]
    table_string = "\n".join(table_list)
    formated_message = SCORE_MESSAGE.substitute(value=score, table=table_string)
    await update.message.reply_text(formated_message, parse_mode=ParseMode.MARKDOWN_V2)
