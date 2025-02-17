" Command handler for the /help command "
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

HELP_MESSAGE = r"""
You want to know more about me? Hmm\.\.\. Have you lost yourself in the labyrinth of your own mind? 🌀
Here are the things you can ask of me during your challenges:

/help — I will show you the way to the light\. 🕯️
/challenge — I will present you with a trial of probability\. 🎲
/solution — I will reveal the secrets of the universe\. 📖
/solution — Choose trials that fit your skills\. 🎯
/remove — I will take back the last trial you have overcome\. 🔄
/score — I will show you the path you have walked\. 📈
/leaderboard — I will show you the path others have walked\. 🏆
"""


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Help command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    await update.message.reply_chat_action("typing")
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)
