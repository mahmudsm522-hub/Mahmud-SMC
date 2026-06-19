import requests

from config.settings import (
    BOT_TOKEN,
    CHAT_ID
)


def send_message(text):

    url = (
        f"https://api.telegram.org/"
        f"bot{BOT_TOKEN}/sendMessage"
    )

    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }

    response = requests.post(
        url,
        json=payload,
        timeout=20
    )

    return response.json()
