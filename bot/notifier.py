import requests

from config.settings import (
    BOT_TOKEN,
    CHAT_ID
)


def send_message(text):

    if not BOT_TOKEN:
        print(
            "[ERROR] BOT_TOKEN missing"
        )
        return None

    if not CHAT_ID:
        print(
            "[ERROR] CHAT_ID missing"
        )
        return None

    try:

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

    except Exception as e:

        print(
            f"[TELEGRAM ERROR] {e}"
        )

        return None
