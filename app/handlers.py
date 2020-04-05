from telegram import ChatAction, Update, PhotoSize, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultPhoto
from telegram.ext import CallbackContext, run_async
from telegram.error import TelegramError, Unauthorized

from copy import deepcopy
from threading import Thread
import validators
import requests
import logging
import re

from .tools import send_action, stop_and_restart, strip, send_mailing, check_username, process_data
from .constants import admin_markup, mailing_markup, main_markup, cancel_markup, lang_markup
from .constants import messages, states
from .database import DataBase
from .statebase import StateBase

import config


# handle all errors related to Telegram
def handle_error(update: Update, context: CallbackContext):
    try:
        raise context.error

    except Unauthorized:
        if update.message:
            with DataBase() as db:
                user_id = update.message.chat_id
                db.del_user(user_id=user_id)

    except TelegramError:
        logging.error(context.error)

        for user_id in config.admins:
            context.bot.send_message(
                chat_id=user_id,
                text=f'<code>UNEXPECTED ERROR: {context.error}.\n\n{update}</code>',
                parse_mode='HTML'
            )

    except KeyError as ex:
        logging.error(ex)


# send owner the admin markup
@send_action(ChatAction.TYPING)
def handle_admin(update: Update, context: CallbackContext):
    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
            context.bot.send_message(
                chat_id=update.message.from_user.id,
                text=messages['admin'][lang],
                reply_markup=admin_markup[lang]
            )


# restart the bot
@send_action(ChatAction.TYPING)
def handle_reboot(update: Update, context: CallbackContext):
    chat_id = update.callback_query.from_user.id
    message_id = update.callback_query.message.message_id

    with DataBase() as db:
        if lang := db.get_value(user_id=chat_id, item='lang'):
            context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=messages['reboot'][lang])
            Thread(target=stop_and_restart).start()


# send statistics about the bot
def handle_statistics(update: Update, context: CallbackContext):
    with DataBase() as db:
        users_amount = db.get_users_amount()
        total_amount = db.get_requests()
        languages = db.get_languages()

        if lang := db.get_value(user_id=update.callback_query.from_user.id, item='lang'):
            context.bot.edit_message_text(
                chat_id=update.callback_query.from_user.id,
                message_id=update.callback_query.message.message_id,
                text=messages['statistics'][lang].format(
                    users_amount, total_amount, *languages.values()
                ),
                reply_markup=InlineKeyboardMarkup([[]]),
                parse_mode='HTML'
            )


# send the mailing form
def handle_mailing(update: Update, context: CallbackContext):
    chat_id = update.callback_query.from_user.id
    message_id = update.callback_query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    with StateBase() as sb:
        empty_data = {'text': None, 'photo': None, 'button': None}
        sb[chat_id] = 'mailing', empty_data

    with DataBase() as db:
        if lang := db.get_value(user_id=chat_id, item='lang'):
            markup = mailing_markup[lang]
            text = messages['mailing'][lang].format(*empty_data.values())

            context.bot.send_message(
                chat_id=chat_id, text=text, reply_markup=markup,
                parse_mode='HTML', disable_web_page_preview=True
            )


# set a state before changing any content for the mailing message
def handle_change_content(update: Update, context: CallbackContext):
    new_state = states[update.message.text]

    with StateBase() as sb:
        response = sb[update.message.from_user.id]
        sb[update.message.from_user.id] = new_state, response['data']

    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
            context.bot.send_message(
                text=messages[new_state][lang],
                chat_id=update.message.from_user.id,
                reply_markup=cancel_markup[lang]
            )


# add content to the message for mailing
def handle_mailing_content(update: Update, context: CallbackContext):
    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
            with StateBase() as sb:
                response = sb[update.message.from_user.id]
                content_type = response['state'].replace('change_', '')

                if content_type == 'text':
                    response['data']['text'] = update.message.text_html

                elif content_type == 'photo':
                    photo = update.message.photo[0]
                    response['data']['photo'] = (photo.file_id, photo.width, photo.height)

                elif content_type == 'button':
                    if '-' in update.message.text:
                        text, url = map(strip, update.message.text.split('-'))

                        if validators.url(url) and requests.get(url).status_code == 200:
                            response['data']['button'] = update.message.text

                        else:
                            context.bot.send_message(
                                chat_id=update.message.chat_id,
                                text=messages['broken_url'][lang],
                                reply_markup=cancel_markup[lang]
                            )
                            return
                    else:
                        context.bot.send_message(
                            chat_id=update.message.chat_id,
                            text=messages['incorrect_button'],
                            reply_markup=cancel_markup[lang]
                        )
                        return

                sb[update.message.from_user.id] = 'mailing', response['data']

            context.bot.send_message(
                chat_id=update.message.from_user.id,
                text=messages['mailing'][lang].format(*response['data'].values()),
                reply_markup=mailing_markup[lang],
                parse_mode='HTML',
                disable_web_page_preview=True
            )


# send mailing to everyone
@run_async
def handle_send_mailing(update: Update, context: CallbackContext):
    with StateBase() as sb:
        response = sb[update.message.from_user.id]
        with DataBase() as db:
            if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):

                mailing = send_mailing(context.bot, response['data'])
                if next(mailing):
                    context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text=messages['started_mailing'][lang],
                        reply_markup=main_markup[lang],
                        parse_mode='HTML'
                    )

                    del sb[update.message.from_user.id]
                    result = next(mailing)

                    context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text=messages['mailing_completed'][lang].format(*result),
                        reply_markup=main_markup[lang],
                        parse_mode='HTML'
                    )

                else:
                    context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text=messages['no_mailing_data'][lang],
                        parse_mode='HTML'
                    )


# send preview of the mailing message
def handle_preview(update: Update, context: CallbackContext):
    with StateBase() as sb:
        response = sb[update.message.from_user.id]
        data = response['data']
        markup = data['button']

        if data['button']:
            text, url = map(strip, markup.split('-'))
            button = InlineKeyboardButton(text, url=url)
            markup = InlineKeyboardMarkup([[button]])

        if data['photo']:
            context.bot.send_photo(
                chat_id=update.message.chat_id,
                photo=PhotoSize(*data['photo']),
                caption=data['text'], parse_mode='HTML',
                reply_markup=markup
            )

        elif data['text']:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=data['text'], parse_mode='HTML',
                reply_markup=markup
            )

        else:
            with DataBase() as db:
                if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
                    context.bot.send_message(
                        chat_id=update.message.chat_id,
                        text=messages['no_mailing_data'][lang],
                        parse_mode='HTML'
                    )


# cancel add content
def handle_cancel_adding(update: Update, context: CallbackContext):
    with StateBase() as sb:
        data = sb[update.message.from_user.id]['data']
        sb[update.message.from_user.id] = 'mailing', data

    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
            context.bot.send_message(
                text=messages['mailing'][lang].format(*data.values()),
                chat_id=update.message.chat_id,
                reply_markup=mailing_markup[lang],
                parse_mode='HTML'
            )


# cancel mailing
def handle_cancel_mailing(update: Update, context: CallbackContext):
    with StateBase() as sb:
        del sb[update.message.from_user.id]

    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=messages['cancel_mailing'][lang],
                reply_markup=main_markup[lang]
            )


# add a new user to the database and send him start message with main markup
@send_action(ChatAction.TYPING)
def handle_start(update: Update, context: CallbackContext):
    with DataBase() as db:
        db.add_user(update.message.from_user.id)
        names = [update.message.from_user.first_name] * 2
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=messages['start'].format(*names),
            reply_markup=lang_markup
        )


# send message with choice of languages
@send_action(ChatAction.TYPING)
def handle_change_lang(update: Update, context: CallbackContext):
    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=messages['current_lang'][lang],
                reply_markup=lang_markup
            )


# change language
def handle_inline_lang(update: Update, context: CallbackContext):
    with DataBase() as db:
        if current_lang := db.get_value(user_id=update.callback_query.message.chat_id, item='lang'):
            new_lang = update.callback_query.data.replace('change_lang_', '')

            try:
                context.bot.delete_message(
                    chat_id=update.callback_query.message.chat_id,
                    message_id=update.callback_query.message.message_id
                )

                context.bot.send_message(
                    chat_id=update.callback_query.message.chat_id,
                    text=messages['changed'][new_lang],
                    reply_markup=main_markup[new_lang]
                )
            except TelegramError:
                return

            if not current_lang == new_lang:
                db.set_value(user_id=update.callback_query.message.chat_id, item='lang', data=new_lang)


# send help message
def handle_help(update: Update, context: CallbackContext):
    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
            with open(f'resources/example_{lang}.png', 'rb') as bytes_photo:
                context.bot.send_photo(
                    chat_id=update.message.chat_id,
                    photo=bytes_photo,
                    caption=messages['usage'][lang],
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )


# send about message
def handle_about(update: Update, context: CallbackContext):
    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=messages['about'][lang],
                parse_mode='HTML',
                disable_web_page_preview=True
            )


# check user's username and send the list
@run_async
def handle_check_my_username(update: Update, context: CallbackContext):
    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):
            if update.message.from_user.username:
                __handle_username(update, context, update.message.from_user.username)

            else:
                context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=messages['no_username'][lang],
                    parse_mode='HTML'
                )


# create Thread for checking username
def handle_username(update: Update, context: CallbackContext):
    username = update.message.text.replace('@', '')
    __handle_username(update, context, username)


# check username and send the list
def __handle_username(update: Update, context: CallbackContext, username: str):
    with DataBase() as db:
        if lang := db.get_value(user_id=update.message.from_user.id, item='lang'):

            if re.match('^[A-Za-z0-9_-]*$', username):
                db.increment(user_id=update.message.from_user.id, item='requests')

                checker = check_username(username)
                prepared_data = process_data(deepcopy(next(checker)), lang)
                prepared_data['username'] = username
                prepared_data['bot_username'] = context.bot.username

                current_message = context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=messages['username_info'][lang].format(**prepared_data),
                    parse_mode='HTML',
                    disable_web_page_preview=True
                )

                for data in checker:
                    prepared_data = process_data(deepcopy(data), lang)
                    prepared_data['username'] = username
                    prepared_data['bot_username'] = context.bot.username

                    try:
                        context.bot.edit_message_text(
                            chat_id=update.message.chat_id,
                            message_id=current_message.message_id,
                            text=messages['username_info'][lang].format(**prepared_data),
                            parse_mode='HTML',
                            disable_web_page_preview=True
                        )
                    except TelegramError:
                        return
            else:
                context.bot.send_message(
                    chat_id=update.message.chat_id,
                    text=messages['invalid_username'][lang],
                    parse_mode='HTML'
            )
