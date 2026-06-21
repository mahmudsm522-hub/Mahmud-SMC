import os

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "CHAT_ID"
)

MAX_WORKERS = int(
    os.getenv(
        "MAX_WORKERS",
        "10"
    )
)

SCAN_INTERVAL = int(
    os.getenv(
        "SCAN_INTERVAL",
        "300"
    )
)
