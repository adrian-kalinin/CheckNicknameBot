from telegram.ext import Updater

from configparser import ConfigParser
import logging

from bot.models import database, User
from bot.callbacks import error_callback

from bot.handlers import (
    start_handler, admin_handler,
    statistics_handler, backup_handler, mailing_conversation_handler
)


# set up logger
logging.basicConfig(
    format='%(asctime)s – %(levelname)s – %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO
)

# parse config
config = ConfigParser()
config.read('config.ini')

# create updater
updater = Updater(config.get('bot', 'token'))
dispatcher = updater.dispatcher


# bound handlers to dispatcher
def bound_handlers():
    # noinspection PyTypeChecker
    dispatcher.add_error_handler(error_callback)

    # command handlers
    dispatcher.add_handler(admin_handler)
    dispatcher.add_handler(start_handler)

    # admin handlers
    dispatcher.add_handler(statistics_handler)
    dispatcher.add_handler(backup_handler)

    # mailing handlers
    dispatcher.add_handler(mailing_conversation_handler)


# set up database
def configure_database():
    database.connect()
    database.create_tables([User])
    database.close()
    logging.info('Database has been configured')


# set up webhook
def configure_webhook():
    pass


def main():
    # setting up application
    bound_handlers()
    configure_database()
    configure_webhook()

    # start bot
    updater.start_polling()
    logging.info('Bot has started')


if __name__ == '__main__':
    main()
