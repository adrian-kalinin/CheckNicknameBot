from bot.utils.constants_old import urls
import requests


def _check_request(link: str):
    response = requests.get(link)
    if response.status_code == 200:
        return link
    return False


def _check_instagram(username: str):
    link = urls['instagram'].format(username)
    return _check_request(link)


def _check_twitter(username: str):
    link = urls['twitter'].format(username)
    return _check_request(link)


def _check_vk(username: str):
    link = urls['vk'].format(username)
    return _check_request(link)


def _check_facebook(username: str):
    link = urls['facebook'].format(username)
    return _check_request(link)


def _check_github(username: str):
    link = urls['github'].format(username)
    return _check_request(link)


def _check_tiktok(username):
    link = urls['tiktok'].format(username)
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
    if 'video-feed' in requests.get(link, headers=headers).text:
        return link
    return False


def _check_telegram(username):
    link = urls['telegram'].format(username)
    if 'tgme_page_title' in requests.get(link).text:
        return link
    return False


checkers = {
    'instagram': _check_instagram,
    'twitter': _check_twitter,
    'vk': _check_vk,
    'facebook': _check_facebook,
    'github': _check_github,
    'tiktok': _check_tiktok,
    'telegram': _check_telegram
}
