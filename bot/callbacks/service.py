from telegram import Update, TelegramError
from telegram.ext import CallbackContext
import logging

from settings import DEVELOPER

from ..constants import Message


# catch errors
def error_callback(update: Update, context: CallbackContext):
    try:
        raise context.error

    except TelegramError as ex:
        logging.error(ex)

        context.bot.send_message(
            chat_id=DEVELOPER,
            text=Message.unexpected_error.format(error=context.error, update=update)
        )

    except Exception as ex:
        logging.error(ex)
