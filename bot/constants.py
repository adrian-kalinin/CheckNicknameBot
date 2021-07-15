from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup


urls = {
    'instagram': 'https://www.instagram.com/{}/',
    'twitter': 'https://twitter.com/{}/',
    'vk': 'https://vk.com/{}/',
    'facebook': 'https://www.facebook.com/{}/',
    'github': 'https://github.com/{}/',
    'telegram': 'https://t.me/{}/',
    'tiktok': 'https://www.tiktok.com/@{}?'
}


class States:
    prepare_mailing = 1
    received_mailing = 2


class CallbackData:
    statistics = 'statistics'
    mailing = 'mailing'
    backup = 'backup'


class ReplyButtons:
    check_my_username = '⚙️ Check my username'
    how_to_use = '💬 How to use?'

    send_mailing = 'Send'
    preview_mailing = 'Preview'
    cancel_mailing = 'Cancel'


class Keyboard:
    main = ReplyKeyboardMarkup([
        [ReplyButtons.check_my_username, ReplyButtons.how_to_use]
    ], resize_keyboard=True)

    admin = InlineKeyboardMarkup([
        [InlineKeyboardButton('View statistics', callback_data=CallbackData.statistics)],
        [InlineKeyboardButton('Create broadcast', callback_data=CallbackData.mailing)]
    ])

    mailing = ReplyKeyboardMarkup([
        [ReplyButtons.send_mailing],
        [ReplyButtons.preview_mailing, ReplyButtons.cancel_mailing]
    ])


class Message:
    start = (
        'Hey there 👋\n\n'
        "Just send me any username and I will check if the it's available on social medias. "
        'Remember that usernames can contain only letters, numbers and underscores.\n\n'
        'Have a good one!'
    )

    how_to_use = (
        "💬 Just send me any username and I will check if the it's available on social medias. "
        'Remember that usernames can contain only letters, numbers and underscores.\n\n'
    )

    invalid_username = '💬 Usernames can only contain letters, numbers, underscores and dashes'

    no_username = "💬 Your profile doesn't have an username, you can set one in the settings"

    admin = 'Welcome to the admin panel!'

    statistics = (
        "Bot's statistics:\n\n"
        'Users in total: <b>{total_users}</b>\n'
        'Active users: <b>{active_users}</b>\n'
        'Number of requests: <b>{total_requests}</b>'
    )

    mailing = 'Send a messaged for the broadcast'

    received_mailing = "The message has been received. What's next?"

    mailing_canceled = 'Broadcast has been cancelled'

    mailing_started = 'Broadcast had started'

    mailing_finished = (
        'Message has been sent:\n\n'
        'Users that received the message: {sent_count}'
    )

    unexpected_error = '<code>Telegram Error: {error}.\n\n{update}</code>'
