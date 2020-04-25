Telegram bot for Evernote
=========================

This bot can save everything that you send to your Evernote account.

# Installation
If you have some reasons do not use my bot deployed on my server, you can use
your own installation.  

* Create your own bot with the
[BotFather](https://telegram.me/BotFather)
(see https://core.telegram.org/bots#3-how-do-i-create-a-bot)
* Create your own Evernote application and obtain a pair of keys (access key and access secret) 
    * Go to https://dev.evernote.com/doc/ and press the green button *"GET AN API KEY"*
* Install a Docker to your server (see https://docs.docker.com/install/)
* Get and set up SSL certificate (see https://letsencrypt.org)
* Set up [nginx](https://nginx.org)/[caddy](https://caddyserver.com)/another proxy server to work with your SSL certificate.
* Check you have *[curl](https://curl.haxx.se/download.html)* on your server (usually it's installed by default)
* Execute this command: `sudo curl https://raw.githubusercontent.com/djudman/evernote-telegram-bot/master/evernotebot-install.sh --output evernotebot-install.sh && sh evernotebot-install.sh`
    * `sudo` is needed because there is copying a file to `/etc/init.d` directory
    * you will need to enter some data as:
        * telegram api token
        * evernote access key
        * evernote access secret
        * etc., see [Environment variables](#Environment-variables)
* Execute `/etc/init.d/evernotebot start` to start bot

## How to build docker image manually

* Clone source code to your server
    ```
    git clone https://github.com/nsuvorov83/evernote-telegram-bot.git
    ```
* Build image
    ```
    docker build -t evernote-telegram-bot .
    ```
* Define [environment variables](#Environment-variables) (for example, in `.bashrc`)
* Create a docker volume to store data
    `docker volume create evernotebot-data`
* Run a container
    ```
    docker run \
        -e EVERNOTEBOT_DEBUG="$EVERNOTEBOT_DEBUG" \
        -e MONGO_HOST="$MONGO_HOST" \
        -e EVERNOTEBOT_HOSTNAME="$EVERNOTEBOT_HOSTNAME" \
        -e TELEGRAM_API_TOKEN="$TELEGRAM_API_TOKEN" \
        -e TELEGRAM_BOT_NAME="$TELEGRAM_BOT_NAME" \
        -e EVERNOTE_BASIC_ACCESS_KEY="$EVERNOTE_BASIC_ACCESS_KEY" \
        -e EVERNOTE_BASIC_ACCESS_SECRET="$EVERNOTE_BASIC_ACCESS_SECRET" \
        -e EVERNOTE_FULL_ACCESS_KEY="$EVERNOTE_FULL_ACCESS_KEY" \
        -e EVERNOTE_FULL_ACCESS_SECRET="$EVERNOTE_FULL_ACCESS_SECRET" \
        -d \
        -p 127.0.0.1:8000:8000 \
        --restart=always \
        --name=evernotebot \
        -it \
        -v ./logs:/app/logs:rw \
        --mount source="evernotebot-data",target="/evernotebot-data" \
        evernote-telegram-bot
    ```

# Environment variables
| Variable name                | Default value | Description |
|------------------------------|---------------|-------------|
| EVERNOTEBOT_DEBUG            | 0             | Enable debug mode (additional logging enabled) |
| EVERNOTEBOT_HOSTNAME         | evernotebot.djudman.info | DNS name of your host
| TELEGRAM_API_TOKEN           | -             | Access token for telegram API. You can obtain this by BotFather |
| TELEGRAM_BOT_NAME            | evernoterobot | Name of telegram bot. You used this in BotFather |
| EVERNOTE_BASIC_ACCESS_KEY    | -             | appKey for your Evernote app (with readonly permissions) |
| EVERNOTE_BASIC_ACCESS_SECRET | -             | secret for your Evernote app (with readonly permissions) |
| EVERNOTE_FULL_ACCESS_KEY     | -             | appKey for your Evernote app (with read/write permissions) |
| EVERNOTE_FULL_ACCESS_SECRET  | -             | secret for your Evernote app (with read/write permissions) |
| MONGO_HOST                   | 127.0.0.1     | Hostname for mongodb host|
