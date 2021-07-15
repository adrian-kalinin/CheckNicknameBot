from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, Filters

from settings import ADMINS

from .constants import CallbackData, States, ReplyButtons
from .callbacks import *


# command handlers
admin_handler = CommandHandler(
    command='admin', callback=admin_command_callback,
    filters=Filters.user(user_id=ADMINS)
)

start_handler = CommandHandler(
    command='start', callback=start_command_callback
)

# admin handlers
statistics_handler = CallbackQueryHandler(
    pattern=CallbackData.statistics,
    callback=statistics_callback
)

# mailing handlers
mailing_conversation_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(pattern=CallbackData.mailing, callback=mailing_callback)],
    states={
        States.prepare_mailing: [MessageHandler(callback=mailing_message_callback, filters=Filters.all)],
        States.received_mailing: [
            MessageHandler(filters=Filters.text(ReplyButtons.preview_mailing), callback=preview_mailing_callback),
            MessageHandler(filters=Filters.text(ReplyButtons.cancel_mailing), callback=cancel_mailing_callback),
            MessageHandler(filters=Filters.text(ReplyButtons.send_mailing), callback=send_mailing_callback)
        ]
    },
    fallbacks=[],
    run_async=True

)

# core handlers
check_my_username_handler = MessageHandler(
    filters=Filters.text(ReplyButtons.check_my_username),
    callback=check_my_username_callback,
    run_async=True
)

how_to_use_handler = MessageHandler(
    filters=Filters.text(ReplyButtons.how_to_use),
    callback=how_to_use_callback
)

check_username_handler = MessageHandler(
    filters=Filters.text,
    callback=check_username_callback,
    run_async=True
)
