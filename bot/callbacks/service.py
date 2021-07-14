from telegram import Update, TelegramError
from telegram.ext import CallbackContext

from configparser import ConfigParser
import logging

from ..constants import Message


# parse config
config = ConfigParser()
config.read('config.ini')


# catch errors
def error_callback(update: Update, context: CallbackContext):
    try:
        raise context.error

    except TelegramError as ex:
        logging.error(ex)

        context.bot.send_message(
            chat_id=config.getint('bot', 'developer'),
            text=Message.unexpected_error.format(error=context.error, update=update)
        )

    except Exception as ex:
        logging.error(ex)
