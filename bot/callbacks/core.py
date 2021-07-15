from telegram import Update, Bot, ParseMode
from telegram.ext import CallbackContext

import re

from ..models import User
from ..constants import Message, USERNAME_STATUSES
from ..utils import checkers


def __check_username(bot: Bot, username: str, user_id: int):
    query = User.update(requests=User.requests + 1).where(User.user_id == user_id)
    query.execute()

    data = {social_media: None for social_media in checkers.keys()}
    statuses = {key + '_status': USERNAME_STATUSES[value]['emoji'] for key, value in data.items()}

    text = Message.result.format(username=username, bot_username=bot.username, **data, **statuses)

    message = bot.send_message(
        chat_id=user_id,
        text=text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

    for social_media in checkers.keys():
        result = checkers[social_media](username)

        if result in [False, None]:
            data[social_media] = USERNAME_STATUSES[result]['text']
            statuses[social_media + '_status'] = USERNAME_STATUSES[result]['emoji']

        else:
            data[social_media] = USERNAME_STATUSES[True]['text'].format(result)
            statuses[social_media + '_status'] = USERNAME_STATUSES[True]['emoji']

        text = Message.result.format(username=username, bot_username=bot.username, **data, **statuses)
        message.edit_text(
            text=text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
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
