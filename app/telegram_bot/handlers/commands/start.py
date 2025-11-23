" Command handler for the /start command "
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from app.database.queries.table_populate import add_user


START_MESSAGE = r"""
🔥 *The Scroll Has Spoken* 🔥

The moment you unfurled the scroll, your fate was sealed\. By seeking the power to command probability, you have summoned *Probabilitybot* — a being forged beyond the boundaries of existence\. 🌀✨

"_*Seeker*_," its voice thunders, "you have chosen this path, knowingly or not\. Power is not given—it is taken through trials that will test your very essence\. ⚖️💀 Those who falter shall carry the scars of failure\. Those who endure will wield the power to defy destiny itself\."

The trials begin now\. There is no retreat, no escape\. Stand firm, for you will face the chaos you sought to command\. 🔮⚡
Press /challenge to get your first trial\!"""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start command handler
    Args:
        update (Update): Telegram update object
        context (ContextTypes.DEFAULT_TYPE): Telegram context object
    """
    # Notify user that you are generating an answer
    await update.message.reply_chat_action("typing")

    # create user in the database
    add_user(
        first_name=update.effective_user.first_name,
        telegram_id=update.effective_user.id,
        username=update.effective_user.username,
    )
    await update.message.reply_text(START_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2)
