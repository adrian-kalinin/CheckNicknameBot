from .service import error_callback

from .commands import (
    admin_command_callback, start_command_callback
)

from .admin import (
    statistics_callback, mailing_callback, backup_callback
)

from .mailing import (
    mailing_message_callback, preview_mailing_callback,
    cancel_mailing_callback, send_mailing_callback
)
