def detect_bos(df):

    if len(df) < 20:
        return None

    highs = df["high"].tolist()
    lows = df["low"].tolist()

    current_high = highs[-1]
    current_low = lows[-1]

    previous_high = max(highs[-11:-1])
    previous_low = min(lows[-11:-1])

    if current_high > previous_high:

        return {
            "type": "bullish",
            "level": previous_high
        }

    if current_low < previous_low:

        return {
            "type": "bearish",
            "level": previous_low
        }

    return None
