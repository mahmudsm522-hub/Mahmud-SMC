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

TOP_SYMBOLS = int(
    os.getenv(
        "TOP_SYMBOLS",
        "100"
    )
)

MAX_FVG_DISTANCE = float(
    os.getenv(
        "MAX_FVG_DISTANCE",
        "2.0"
    )
)
