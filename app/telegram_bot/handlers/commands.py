from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from string import Template

START_MESSAGE = r"""
🔥 *The Scroll Has Spoken* 🔥

The moment you unfurled the scroll, your fate was sealed\. By seeking the power to command probability, you have summoned *Probabilitybot* — a being forged beyond the boundaries of existence\. 🌀✨

"_*Seeker*_," its voice thunders, "you have chosen this path, knowingly or not\. Power is not given—it is taken through trials that will test your very essence\. ⚖️💀 Those who falter shall carry the scars of failure\. Those who endure will wield the power to defy destiny itself\."

The trials begin now\. There is no retreat, no escape\. Stand firm, for you will face the chaos you sought to command\. 🔮⚡"""


HELP_MESSAGE = r"""
You want to know more about me? Hmm\.\.\. Have you lost yourself in the labyrinth of your own mind? 🌀
Here are the things you can ask of me during your challenges:

/help — I will show you the way to the light\. 🕯️
/challenge — I will present you with a trial of probability\. 🎲
/solution — I will reveal the secrets of the universe\. 📖
/score — I will show you the path you have walked\. 📈
/leaderboard — I will show you the path others have walked\. 🏆
"""

CHALLENGE_MESSAGE = "Here comes another trial\! 🎲"

SCORE_MESSAGE = Template(
    "Let me see\.\. Hmm\.\. Through you challenges you have gained $value points of cassuality\! 🌀🔢"
)

LEADERBOARD_MESSAGE = "Here are the top 5 challengers of this trial\! 🏆"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)


async def challenge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CHALLENGE_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)


async def score_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    value = 100
    formated_message = SCORE_MESSAGE.substitute(value=value)
    await update.message.reply_text(formated_message, parse_mode=ParseMode.MARKDOWN_V2)


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        LEADERBOARD_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2
    )
