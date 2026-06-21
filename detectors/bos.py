from utils.candles import (
    find_swing_highs,
    find_swing_lows
)


def detect_bos(df):

    if len(df) < 50:
        return None

    swing_highs = find_swing_highs(df)
    swing_lows = find_swing_lows(df)

    if len(swing_highs) < 2:
        return None

    if len(swing_lows) < 2:
        return None

    current_close = float(
        df.iloc[-1]["close"]
    )

    last_high = swing_highs[-1]
    last_low = swing_lows[-1]

    # Bullish BOS

    if current_close > last_high["price"]:

        return {
            "direction": "bullish",
            "level": last_high["price"],
            "close": current_close,
            "swing_index": last_high["index"]
        }

    # Bearish BOS

    if current_close < last_low["price"]:

        return {
            "direction": "bearish",
            "level": last_low["price"],
            "close": current_close,
            "swing_index": last_low["index"]
        }

    return None
