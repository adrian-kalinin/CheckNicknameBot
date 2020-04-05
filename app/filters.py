from telegram.ext import BaseFilter

from .statebase import StateBase


class MailingFilter(BaseFilter):
    def filter(self, message):
        with StateBase() as sb:
            response = sb[message.from_user.id]
            if isinstance(response, dict):
                return response['state'] == 'mailing'


class AddingFilter(BaseFilter):
    def filter(self, message):
        with StateBase() as sb:
            response = sb[message.from_user.id]
            if isinstance(response, dict):
                return 'add_' in response['state']


# initialize custom filters
mailing_filter = MailingFilter()
adding_filter = AddingFilter()
