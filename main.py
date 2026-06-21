import time
import traceback

from data.bybit_fetcher import (
    get_symbols,
    get_klines
)

from signals.signal_manager import (
    validate_signal,
    build_signal_message
)

from telegram.notifier import (
    send_message
)

from utils.signal_cache import (
    signal_exists,
    add_signal
)


SCAN_INTERVAL = 60


def process_symbol(symbol):

    try:

        h1_df = get_klines(
            symbol=symbol,
            interval="60"
        )

        m15_df = get_klines(
            symbol=symbol,
            interval="15"
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

    symbols = get_symbols()

    print(
        f"Scanning {len(symbols)} symbols..."
    )

    for symbol in symbols:

        process_symbol(symbol)


def main():

    send_message(
        "🚀 SMC Bot Started"
    )

    while True:

        try:

            scan_market()

            print(
                "Scan complete"
            )

            time.sleep(
                SCAN_INTERVAL
            )

        except Exception:

            traceback.print_exc()

            time.sleep(30)


if __name__ == "__main__":
    main()
