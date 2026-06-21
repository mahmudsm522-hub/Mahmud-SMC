from utils.candles import (
    find_swing_highs,
    find_swing_lows
)


def detect_choch(df):

    if len(df) < 60:
        return None

    swing_highs = find_swing_highs(df)
    swing_lows = find_swing_lows(df)

    if len(swing_highs) < 3:
        return None

    if len(swing_lows) < 3:
        return None

    current_close = float(
        df.iloc[-1]["close"]
    )

    last_high = swing_highs[-1]
    prev_high = swing_highs[-2]

    last_low = swing_lows[-1]
    prev_low = swing_lows[-2]

    # Bullish CHoCH
    # Higher Low + Break High

    if (
        last_low["price"] >
        prev_low["price"]
        and
        current_close >
        last_high["price"]
    ):

        return {
            "direction": "bullish",
            "break_level": last_high["price"],
            "close": current_close,
            "swing_index": last_high["index"]
        }

    # Bearish CHoCH
    # Lower High + Break Low

    if (
        last_high["price"] <
        prev_high["price"]
        and
        current_close <
        last_low["price"]
    ):

        return {
            "direction": "bearish",
            "break_level": last_low["price"],
            "close": current_close,
            "swing_index": last_low["index"]
        }

    return None
