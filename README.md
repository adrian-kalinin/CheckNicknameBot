# CheckNicknameBot
Telegram bot that checks if an username is available in social networks.

# User Usage

Everything is pretty simple – just send an username to the bot; or press the button if you want to check your own.

![Example](https://github.com/adreex/CheckNicknameBot/blob/master/resources/example_en.png)

# Admin Usage

There are some features for admins of the bot. Firt off all, you should enter `/admin` command. Then you can check statistics and restart the bot.

![Admin panel](https://github.com/adreex/CheckNicknameBot/blob/master/resources/readme_admin.png)

One more great feature is the possibility to send a message to all the users.

![Mailing](https://github.com/adreex/CheckNicknameBot/blob/master/resources/readme_mailing.png)

# Deployment

### Configurate `config.py`:

Create a new Telegram Bot at t.me/BotFather and get the token of your bot, then put it as `token` variable.
Then you can enter for `admins` some ids of users who can use the admins' commands.
Fill your `host` (server's ip) and `port` (443, 80, 88 or 8443).

### Generate quick'n'dirty SSL certificate (in terminal):

`openssl genrsa -out webhook_pkey.pem 2048`

`openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem`

Attention! When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply with the same value as your server's ip addres.

### Create virtual environment for Python and install all requiremetns (in terminal):

`virtualenv venv --python=python3`

`source venv/bin/activate`

`pip install -r requiremetns.txt`

Just enter `python main.py` in your terminal.
