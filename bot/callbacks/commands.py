from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from ..models import User
from ..constants import Message, Keyboard


def admin_command_callback(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=Message.admin, reply_markup=Keyboard.admin
    )


def start_command_callback(update: Update, context: CallbackContext):
    user, created = User.get_or_create(user_id=update.effective_user.id)

    if not user.active:
        user.active = True
        user.save()

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=Message.start, parse_mode=ParseMode.HTML,
        reply_markup=Keyboard.main
    )
