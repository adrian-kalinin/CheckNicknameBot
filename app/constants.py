from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import config

# urls

urls = {
    'instagram': 'https://www.instagram.com/{}/',
    'twitter': 'https://twitter.com/{}/',
    'vk': 'https://vk.com/{}/',
    'facebook': 'https://www.facebook.com/{}/',
    'github': 'https://github.com/{}/',
    'telegram': 'https://t.me/{}/',
    'tiktok': 'https://www.tiktok.com/@{}?'
}

# username statuses

username_statuses = {
    True: {
        'en': '<a href="{}">unavailable</a>',
        'ru': '<a href="{}">занято</a>'
    },

    False: {
        'en': '<b>available</b>',
        'ru': '<b>доступно</b>'
    },

    None: {
        'en': 'in process',
        'ru': 'в процессе'
    }
}


# main markup

main_buttons = {
    'en': [
        ['⚙️ Check My Username'],
        ['🇬🇧 Change Language', '💬 How to use?']
    ],
    'ru': [
        ['⚙️ Проверить мой юзернейм'],
        ['🇷🇺 Сменить язык', '💬 Как использовать?']
    ]
}

main_markup = {
    'en': ReplyKeyboardMarkup(main_buttons['en'], resize_keyboard=True),
    'ru': ReplyKeyboardMarkup(main_buttons['ru'], resize_keyboard=True)
}

# inline language keyboard

en_button = InlineKeyboardButton(text='English 🇬🇧', callback_data='change_lang_en')
ru_button = InlineKeyboardButton(text='Русский 🇷🇺', callback_data='change_lang_ru')
lang_markup = InlineKeyboardMarkup([[en_button, ru_button]])

# callbacks

reboot_callback = 'reboot'
mailing_callback = 'mailing'
statistics_callback = 'statistics'

# admin markup

admin_keyboard = {
    'en': [
        [InlineKeyboardButton(text='Check Statistics', callback_data=statistics_callback)],
        [InlineKeyboardButton(text='Send Mailing', callback_data=mailing_callback)],
        [InlineKeyboardButton(text='Restart the Bot', callback_data=reboot_callback)]
    ],
    'ru': [
        [InlineKeyboardButton(text='Посмотреть статистику', callback_data=statistics_callback)],
        [InlineKeyboardButton(text='Создать рассылку', callback_data=mailing_callback)],
        [InlineKeyboardButton(text='Перезагрузить бота', callback_data=reboot_callback)]
    ]
}

admin_markup = {
    'en': InlineKeyboardMarkup(admin_keyboard['en']),
    'ru': InlineKeyboardMarkup(admin_keyboard['ru'])
}

# mailing markup

mailing_keyboard = {
    'en': [
        ['Send Message', 'Preview'],
        ['Change Text', 'Change Photo'],
        ['Change Button', 'Cancel Mailing']
    ],
    'ru': [
        ['Разослать сообщение', 'Предпросмотр'],
        ['Изменить текст', 'Изменить фото'],
        ['Изменить кнопку', 'Отменить рассылку']
    ]
}

mailing_markup = {
    'en': ReplyKeyboardMarkup(mailing_keyboard['en'], resize_keyboard=True),
    'ru': ReplyKeyboardMarkup(mailing_keyboard['ru'], resize_keyboard=True)
}

# cancel markup

cancel_keyboard = {
    'en': [['Cancel']],
    'ru': [['Отмена']]
}

cancel_markup = {
    'en': ReplyKeyboardMarkup(cancel_keyboard['en'], resize_keyboard=True),
    'ru': ReplyKeyboardMarkup(cancel_keyboard['ru'], resize_keyboard=True)
}

# commands

admin_command = 'admin'
start_command = 'start'
help_command = 'help'
about_command = 'about'
lang_command = 'lang'

# buttons

check_my_username_button = '({})|({})'.format(*(item[0][0] for item in main_buttons.values()))
lang_button = '({})|({})'.format(*(item[1][0] for item in main_buttons.values()))
help_button = '({})|({})'.format(*(item[1][1] for item in main_buttons.values()))

send_mailing_button = '({})|({})'.format(*(item[0][0] for item in mailing_keyboard.values()))
preview_button = '({})|({})'.format(*(item[0][1] for item in mailing_keyboard.values()))
add_text_button = '({})|({})'.format(*(item[1][0] for item in mailing_keyboard.values()))
add_photo_button = '({})|({})'.format(*(item[1][1] for item in mailing_keyboard.values()))
add_button_button = '({})|({})'.format(*(item[2][0] for item in mailing_keyboard.values()))
cancel_mailing_button = '({})|({})'.format(*(item[2][1] for item in mailing_keyboard.values()))

add_content_button = '|'.join([add_text_button, add_photo_button, add_button_button])

cancel_adding_button = '({})|({})'.format(*(item[0][0] for item in cancel_keyboard.values()))

lang_inline_button = '(change_lang_en)|(change_lang_ru)'

# mailing states

states = {
    mailing_keyboard['en'][1][0]: 'change_text',
    mailing_keyboard['ru'][1][0]: 'change_text',
    mailing_keyboard['en'][1][1]: 'change_photo',
    mailing_keyboard['ru'][1][1]: 'change_photo',
    mailing_keyboard['en'][2][0]: 'change_button',
    mailing_keyboard['ru'][2][0]: 'change_button'
}

# messages

messages = {
    'start': '🇬🇧 Welcome, {}! Choose your language to continue.\n\n'
             '🇷🇺 Приветствуем, {}! Для продолжения выберите свой язык.',

    'no_username': {
        'en': '💬 Your profile does not have username.',
        'ru': '💬 Ваш профиль не имеет юзернейма.'
    },

    'username_info': {
        'en': 'Information about the availability of the username <b>{username}</b> in social networks:\n\n'
              '{instagram_status} Instagram: {instagram}\n'
              '{twitter_status} Twitter: {twitter}\n'
              '{vk_status} Vkontakte: {vk}\n'
              '{facebook_status} Facebook: {facebook}\n'
              '{github_status} Github: {github}\n'
              '{tiktok_status} Tiktok: {tiktok}\n'
              '{telegram_status} Telegram: {telegram}\n\n'
              '@{bot_username}',
        'ru': 'Информация о доступности юзернейма <b>{username}</b> в социальных сетях:\n\n'
              '{instagram_status} Instagram: {instagram}\n'
              '{twitter_status} Twitter: {twitter}\n'
              '{vk_status} Vkontakte: {vk}\n'
              '{facebook_status} Facebook: {facebook}\n'
              '{github_status} Github: {github}\n'
              '{tiktok_status} Tiktok: {tiktok}\n'
              '{telegram_status} Telegram: {telegram}\n\n'
              '@{bot_username}',
    },

    'usage': {
        'en': 'To check if the username is available or not on social networks, just send this username to the bot. '
              'However, you should remember that usernames can contain only letters, '
              'numbers and underscores.\n\nHere is an example of usage on the picture.',
        'ru': 'Для того, чтобы проверить, занят юзернейм в социальных сетях, достаточно всего лишь отправить этот '
              'юзернейм боту. Однако следует помнить, что юзернеймы могут содержать '
              'только буквы, цифры и нижние подчеркивания.\n\n'
              'На картинке вы можете посмотреть пример использования.'
    },

    'about': {
        'en': 'This bot was created not for commercial purposes, but with the intent to benefit others.\n\n'
              f'So that I will be glad to receive some donations to pay my servers – {config.yandex_url}',
        'ru': 'Этот бот был создан не с коммерческой целью, а с помыслом принести пользу остальным.\n\n'
              f'Поэтому я буду рад получить любую денежную поддержку для оплаты моих серверов – {config.yandex_url}.'
    },

    'invalid_username': {
      'en': '💬 Username can only contain letters, numbers, underscores and dashes.',
      'ru': '💬 Юзернейм может содержать только буквы, цифры, нижние подчеркивания и тире.'
    },

    'admin': {
        'en': 'Welcome back, Creator! 🖤',
        'ru': 'С возвращением, создатель! 🖤'
    },

    'reboot': {
        'en': 'The bot has been restarted',
        'ru': 'Бот успешно перезагружен'
    },

    'statistics': {
        'en': 'Here are some statistics about the bot:\n\n'
              'The number of users: <b>{}</b>\n'
              'Total requests amount: <b>{}</b>\n\n'
              'Statistics on languages:\n\n'
              '🇬🇧 – <b>{}</b>\n'
              '🇷🇺 – <b>{}</b>',
        'ru': 'Вот немного статистики о боте:\n\n'
              'Количество пользователей: <b>{}</b>\n'
              'Суммарное число запросов: <b>{}</b>\n\n'
              'Статистика по языкам:\n\n'
              '🇬🇧 – <b>{}</b>\n'
              '🇷🇺 – <b>{}</b>'
    },

    'mailing': {
        'en': '<i>The message for the mailing:</i>\n\n'
              '<b>Text:</b>\n\n{}\n\n'
              '<b>Photo:</b>\n\n<code>{}</code>\n\n'
              '<b>Button:</b>\n\n{}',
        'ru': '<i>Сообщение для массовой рассылки:</i>\n\n'
              '<b>Текст:</b>\n\n{}\n\n'
              '<b>Фото:</b>\n\n<code>{}</code>\n\n'
              '<b>Кнопка:</b>\n\n{}'
    },

    'cancel_mailing': {
        'en': 'The mailing has been canceled.',
        'ru': 'Массовая рассылка отменена.'
    },

    'no_mailing_data': {
        'en': 'Not enough data to send the message.',
        'ru': 'Не хватает данных для отправки сообщения.'
    },

    'mailing_completed': {
        'en': 'The message has been successfully sent:\n\n'
              'Users who received the message: <b>{}</b>\n'
              'Deleted users who blocked the bot: <b>{}</b>',
        'ru': 'Сообщение было успешно отправлено:\n\n'
              'Пользователи, получившие сообщение: <b>{}</b>\n'
              'Удаленные пользователи, которые заблокировали бота: <b>{}</b>'
    },

    'change_text': {
        'en': 'Enter the text which will be attached to the mailing list:',
        'ru': 'Введите текст, который будет прикреплен к сообщению для рассылки:'
    },

    'change_photo': {
        'en': 'Send a picture which will be attached to the message for the mailing:',
        'ru': 'Пришлите картинку, которая будет прикреплена к сообщению для рассылки:'
    },

    'change_button': {
        'en': 'Send a button which will be attached to the message for the newsletter in the format "text - full link":',
        'ru': 'Пришлите кнопку, которая будет прикреплена к сообщению для рассылки в формате "текст - полная ссылка":'
    },

    'broken_url': {
        'rn': 'This link does not work, please retry the request:',
        'ru': 'Данная ссылка не работает, повторите запрос:'
    },

    'incorrect_button': {
        'en': 'The input format does not match, retry the request:',
        'ru': 'Формат ввода не соответствует, повторите запрос:'
    },

    'invalid_tags': {
        'en': 'Make sure all your HTML-tags are valid.',
        'ru': 'Убедитесь, что все ваши HTML-теги корректны.'
    },

    'current_lang': {
        'en': 'Current language is English 🇬🇧',
        'ru': 'Текущий язык Русский 🇷🇺'
    },

    'changed': {
        'en': 'Language has been changed to English 🇬🇧',
        'ru': 'Язык был изменен на Русский 🇷🇺'
    },

    'started_mailing': {
        'en': 'The mailing successfully started',
        'ru': 'Рассылка успешно началась'
    }
}
