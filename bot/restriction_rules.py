import logging
import config

from telegram.update import Update
from telegram.ext import CallbackContext

from functools import wraps

logger = logging.getLogger(__name__)


def only_owner(func):
    @wraps(func)
    def wrapped(update: Update, context: CallbackContext, *args, **kwargs) -> None:
        user_id = update.effective_user.id
        if int(user_id) != int(config.OWNER_ID):
            logger.info("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped
