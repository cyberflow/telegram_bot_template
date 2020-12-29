import logging

from core import bot_handler, get_lazy_handlers

from telegram.ext import CallbackContext, MessageHandler, Filters
from telegram.update import Update


logger = logging.getLogger(__name__)

WELCOME_MESSAGE="""Welcome, @{}!"""


def welcome_new_users(update: Update, context: CallbackContext):
    """Sending welcom message for new users"""
    for user in update.message.new_chat_members:
        if not user.is_bot: # Ignorin welcome bot's
            logger.debug(f"New user {user.username} join to group")
            welcome_text = WELCOME_MESSAGE.format(user.username)
            context.bot.send_message(chat_id=update.message.chat.id, text=welcome_text)

@bot_handler
def welcome_new_users_factory():
    return MessageHandler(
        Filters.status_update.new_chat_members,
        welcome_new_users
    )
