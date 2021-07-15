
username_statuses = {
    True: {
        'emoji': '',
        'text': '<a href="{}">unavailable</a>'
    },

    False: {
        'emoji': '',
        'text': 'available'
    },

    None:  {
        'emoji': '',
        'text': 'in progress...'
    }
}

a = (
    'Information about the availability of the username <b>{username}</b> in social networks:\n\n'
    '{instagram_status} Instagram: {instagram}\n'
    '{twitter_status} Twitter: {twitter}\n'
    '{vk_status} Vkontakte: {vk}\n'
    '{facebook_status} Facebook: {facebook}\n'
    '{github_status} Github: {github}\n'
    '{tiktok_status} Tiktok: {tiktok}\n'
    '{telegram_status} Telegram: {telegram}\n\n'
    '@{bot_username}',
)
