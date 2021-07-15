from telegram import Update, Bot
from telegram.ext import CallbackContext

import re

from ..models import User
from ..constants import Message


def __check_username(bot: Bot, username: str, user_id: int):
    query = User.update(requests=User.requests + 1).where(User.user_id == user_id)
    query.execute()

    # TODO

    bot.send_message(
        chat_id=user_id,
        text='...'  # TODO
    )


def check_username_callback(update: Update, context: CallbackContext):
    username = update.message.text.strip(' ')

    if re.match('^[A-Za-z0-9_-]*$', username) and username.lower() != 'admin':
        __check_username(context.bot, username, update.effective_user.id)

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Message.invalid_username
        )


def check_my_username_callback(update: Update, context: CallbackContext):
    if username := update.effective_user.username:
        __check_username(context.bot, username, update.effective_chat.id)

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Message.no_username
        )


def how_to_use_callback(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=Message.how_to_use
    )
