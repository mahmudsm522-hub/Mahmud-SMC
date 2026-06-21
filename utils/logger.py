import logging
import os

LOG_DIR = "logs"

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

LOG_FILE = (
    f"{LOG_DIR}/bot.log"
)

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    ),
    handlers=[
        logging.FileHandler(
            LOG_FILE
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(
    "SMC_BOT"
)
