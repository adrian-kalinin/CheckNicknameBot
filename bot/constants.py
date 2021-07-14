from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup


class States:
    prepare_mailing = 1
    received_mailing = 2


class CallbackData:
    statistics = 'statistics'
    mailing = 'mailing'
    backup = 'backup'


class ReplyButtons:
    send_mailing = 'Send'
    preview_mailing = 'Preview'
    cancel_mailing = 'Cancel'


class Keyboard:
    main = ReplyKeyboardMarkup([
        ['/start']
    ])

    admin = InlineKeyboardMarkup([
        [InlineKeyboardButton('Check statistics', callback_data=CallbackData.statistics)],
        [InlineKeyboardButton('Create broadcast', callback_data=CallbackData.mailing)],
        [InlineKeyboardButton('Backup database', callback_data=CallbackData.backup)]
    ])

    mailing = ReplyKeyboardMarkup([
        [ReplyButtons.send_mailing],
        [ReplyButtons.preview_mailing, ReplyButtons.cancel_mailing]
    ])


class Message:
    start = '<b>Hello there!</b>'

    admin = 'Welcome to the admin panel!'

    statistics = (
        "Bot's statistics:\n\n"
        'Users in total: <b>{total_users}</b>\n'
        'Active users: <b>{active_users}</b>'
    )

    mailing = 'Send a messaged for the broadcast'

    received_mailing = "The message has been received. What's next?"

    mailing_canceled = 'Broadcast has been cancelled'

    mailing_started = 'Broadcast had started'

    mailing_finished = (
        'Message has been sent:\n\n'
        'Users that perceived the message: {sent_count}'
    )

    unexpected_error = '<code>Telegram Error: {error}.\n\n{update}</code>'

    backup = 'Backup of the database ({})'

    database_not_found = 'Database not found'
