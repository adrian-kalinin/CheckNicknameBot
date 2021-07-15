import environ


env = environ.Env()

READ_DOT_ENV_FILE = env.bool('READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    environ.Env.read_env()

DEBUG = env.bool('DEBUG', False)

BOT_TOKEN = env('BOT_TOKEN')
ADMINS = list(map(int, env.list('ADMINS')))
DEVELOPER = env.int('DEVELOPER')

if not DEBUG:
    DB_NAME = env('DB_NAME')
    DB_USER = env('DB_USER')
    DB_PASSWORD = env('DB_PASSWORD')
    DB_HOST = env('DB_HOST')
    DB_PORT = env.int('DB_PORT')

else:
    SQLITE_DB_PATH = env('SQLITE_DB_PATH')
