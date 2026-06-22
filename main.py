import time
import traceback

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

from data.bybit_fetcher import (
    get_top_symbols_by_volume,
    get_klines
)

from utils.database import (
    init_db
)

from signals.signal_manager import (
    validate_signal,
    build_signal_message
)

from bot.notifier import (
    send_message
)

from utils.signal_cache import (
    signal_exists,
    add_signal
)

MAX_WORKERS = 10
SCAN_INTERVAL = 300


def process_symbol(symbol):

    try:

        h1_df = get_klines(
            symbol=symbol,
            interval="60",
            limit=200
        )

        m15_df = get_klines(
            symbol=symbol,
            interval="15",
            limit=200
        )

        signal = validate_signal(
            symbol=symbol,
            h1_df=h1_df,
            m15_df=m15_df
        )

        if signal is None:
            return

        side = signal["side"]

        zone_start = signal["fvg"]["start"]
        zone_end = signal["fvg"]["end"]

        if signal_exists(
            symbol,
            side,
            zone_start,
            zone_end
        ):
            return

        message = build_signal_message(
            signal
        )

        send_message(message)

        add_signal(
            symbol,
            side,
            zone_start,
            zone_end
        )

        print(
            f"[ALERT] {symbol} {side}"
        )

    except Exception as e:

        print(
            f"[ERROR] {symbol}"
        )

        print(str(e))


def scan_market():

    symbols = get_top_symbols_by_volume(
        limit=100
    )

    print(
        f"Total Symbols: {len(symbols)}"
    )

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = [
            executor.submit(
                process_symbol,
                symbol
            )
            for symbol in symbols
        ]

        for future in as_completed(
            futures
        ):

            try:

                future.result()

            except Exception:

                traceback.print_exc()


def startup_message():

    try:

        send_message(
            """
🚀 SMC BOT ONLINE

Market:
Bybit Futures

Trend:
H1

Entry:
M15

Scanner:
Top USDT Pairs
"""
        )

    except Exception:

        pass


def main():

    init_db()

    startup_message()

    while True:

        try:

            start = time.time()

            print(
                "\n===== NEW SCAN ====="
            )

            scan_market()

            elapsed = (
                time.time() - start
            )

            print(
                f"Scan Time: "
                f"{elapsed:.2f}s"
            )

            print(
                f"Sleeping "
                f"{SCAN_INTERVAL}s"
            )

            time.sleep(
                SCAN_INTERVAL
            )

        except Exception:

            traceback.print_exc()

            time.sleep(60)


if __name__ == "__main__":
    main()
