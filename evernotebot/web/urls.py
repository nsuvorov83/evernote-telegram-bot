from urllib.parse import urlparse

from evernotebot.config import load_config
from evernotebot.web.views import telegram_hook, evernote_oauth


config = load_config()
webhook_url = config["webhook_url"]
webhook_path = urlparse(webhook_url).path

urls = (
    ("POST", webhook_path, telegram_hook),
    ("GET", r"^/evernote/oauth$", evernote_oauth),
)
