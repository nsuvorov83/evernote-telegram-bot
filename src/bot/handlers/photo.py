from os.path import basename
from os.path import join
from urllib.parse import urlparse

from bot.models import User
from util.http import make_request


def handle_photo(bot, telegram_message):
    max_size = 20 * 1024 * 1024 # telegram restriction. We can't download any file that has size more than 20Mb
    file_id = None
    for photo in sorted(telegram_message.photo, key=lambda x: x.file_size, reverse=True):
        if photo.file_size > max_size:
            continue
        file_id = photo.file_id
        break  # NOTE: File with the biggest size found
    if not file_id:
        raise Exception('File too big. Telegram does not allow to the bot to download files over 20Mb.')
    download_url = bot.api.getFile(file_id)
    data = make_request(download_url)
    filename = join(bot.config['tmp_root'], '{0}_{1}'.format(file_id, basename(urlparse(download_url).path)))
    with open(filename, 'wb') as f:
        f.write(data)
    user_id = telegram_message.from_user.id
    user = bot.get_storage(User).get(user_id)
    bot.evernote.create_note(
        user.evernote.access_token,
        user.evernote.notebook.guid,
        telegram_message.text,
        telegram_message.caption or telegram_message.text[:20] or 'Photo',
        (filename,)
    )

