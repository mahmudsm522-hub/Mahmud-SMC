import json
import os
from datetime import datetime

CACHE_FILE = "signal_cache.json"


def load_cache():

    if not os.path.exists(CACHE_FILE):
        return {}

    try:

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        return {}


def save_cache(cache):

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            cache,
            f,
            indent=4
        )


def build_key(
    symbol,
    side,
    zone_start,
    zone_end
):

    return (
        f"{symbol}_"
        f"{side}_"
        f"{round(zone_start, 6)}_"
        f"{round(zone_end, 6)}"
    )


def signal_exists(
    symbol,
    side,
    zone_start,
    zone_end
):

    cache = load_cache()

    key = build_key(
        symbol,
        side,
        zone_start,
        zone_end
    )

    return key in cache


def add_signal(
    symbol,
    side,
    zone_start,
    zone_end
):

    cache = load_cache()

    key = build_key(
        symbol,
        side,
        zone_start,
        zone_end
    )

    cache[key] = {
        "symbol": symbol,
        "side": side,
        "zone_start": zone_start,
        "zone_end": zone_end,
        "created_at": str(
            datetime.utcnow()
        )
    }

    save_cache(cache)


def clear_cache():

    save_cache({})
