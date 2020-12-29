#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
import config

from telegram.ext import Updater

from telegram.error import TelegramError
from core import autodiscovery, get_handlers

logger = logging.getLogger(__name__)


def init_log(log_level):
    if log_level == 'debug':
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s [%(funcName)s] %(message)s'
        )
        logger.debug("Debug level On.")
    else:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s [%(funcName)s] %(message)s'
        )


def error(update, context):
    try:
        raise context.error
    except TelegramError:
        logger.exception("A Telegram error occurred")
    except Exception:
        logger.exception("A general error occurred")
    finally:
        update.effective_message.reply_text('Errors happen ¯\\_(ツ)_/¯')
        # msg_admin(context.bot, 'An error occurred on the bot. Check the logs')

def add_update_handlers(dp):
    for handler in get_handlers():
        dp.add_handler(handler)
    return dp



def main():
    updater = Updater(config.TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add main command handlers
    autodiscovery()
    dispatcher = add_update_handlers(dispatcher)

    # Also add our "log everything" error handler
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    return 0


if __name__ == '__main__':
    try:
        if '--debug' in sys.argv:
            debug_level = 'debug'
        else:
            debug_level = None
        init_log(debug_level)

        sys.exit(main())
    except Exception as e:
        logger.error("An update broke the bot.", exc_info=True)
        sys.exit(-1)
