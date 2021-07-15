from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from peewee import fn

from ..models import User
from ..constants import Message, States


def statistics_callback(update: Update, context: CallbackContext):
    total_users = User.select().count()
    active_users = User.select().where(User.active == True).count()
    total_requests = User.select(fn.sum(User.requests).alias('total')).dicts()[0].get('total')

    response = Message.statistics.format(
        total_users=total_users,
        active_users=active_users,
        total_requests=total_requests
    )

    context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.message_id,
        text=response, parse_mode=ParseMode.HTML
    )


def mailing_callback(update: Update, context: CallbackContext):
    context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=update.effective_message.message_id,
        text=Message.mailing
    )

    return States.prepare_mailing
