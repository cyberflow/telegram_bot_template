from core import bot_handler, get_lazy_handlers

from telegram.ext import CallbackContext, CommandHandler, Filters
from telegram.update import Update


def cmd_help(update: Update, context: CallbackContext):
    out = "Bot commands:\n"
    for handler in get_lazy_handlers():
        doc = handler.__doc__
        if doc:
            out += f"{doc.strip()}\n"
    context.bot.send_message(
            chat_id=update.message.from_user.id,
            text=out
        )


@bot_handler
def help_factory():
    """
    /help - this command show docs for all commands available
    """
    return CommandHandler("help", cmd_help, filters=Filters.chat_type.private)
