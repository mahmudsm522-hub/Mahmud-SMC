# detectors/fvg.py

def detect_fvg(df):

    if len(df) < 10:
        return None

    fvg_list = []

    for i in range(2, len(df)):

        candle_1 = df.iloc[i - 2]
        candle_2 = df.iloc[i - 1]
        candle_3 = df.iloc[i]

        high_1 = float(candle_1["high"])
        low_1 = float(candle_1["low"])

        high_3 = float(candle_3["high"])
        low_3 = float(candle_3["low"])

        # Bullish FVG
        if low_3 > high_1:

            gap_size = low_3 - high_1

            fvg_list.append({
                "type": "bullish",
                "start": high_1,
                "end": low_3,
                "size": gap_size,
                "index": i
            })

        # Bearish FVG
        elif high_3 < low_1:

            gap_size = low_1 - high_3

            fvg_list.append({
                "type": "bearish",
                "start": high_3,
                "end": low_1,
                "size": gap_size,
                "index": i
            })

    if not fvg_list:
        return None

    return fvg_list[-1]


def get_all_fvg(df):

    if len(df) < 10:
        return []

    results = []

    for i in range(2, len(df)):

        candle_1 = df.iloc[i - 2]
        candle_3 = df.iloc[i]

        high_1 = float(candle_1["high"])
        low_1 = float(candle_1["low"])

        high_3 = float(candle_3["high"])
        low_3 = float(candle_3["low"])

        # Bullish FVG
        if low_3 > high_1:

            results.append({
                "type": "bullish",
                "start": high_1,
                "end": low_3,
                "size": low_3 - high_1,
                "index": i
            })

        # Bearish FVG
        elif high_3 < low_1:

            results.append({
                "type": "bearish",
                "start": high_3,
                "end": low_1,
                "size": low_1 - high_3,
                "index": i
            })

    return results


def get_latest_bullish_fvg(df):

    fvgs = get_all_fvg(df)

    bullish = [
        fvg
        for fvg in fvgs
        if fvg["type"] == "bullish"
    ]

    if not bullish:
        return None

    return bullish[-1]


def get_latest_bearish_fvg(df):

    fvgs = get_all_fvg(df)

    bearish = [
        fvg
        for fvg in fvgs
        if fvg["type"] == "bearish"
    ]

    if not bearish:
        return None

    return bearish[-1]


def is_price_inside_fvg(df, fvg):

    if not fvg:
        return False

    current_price = float(
        df.iloc[-1]["close"]
    )

    return (
        fvg["start"]
        <= current_price
        <= fvg["end"]
    )


def get_fvg_summary(df):

    latest = detect_fvg(df)

    if not latest:
        return None

    return {
        "direction": latest["type"],
        "zone_start": latest["start"],
        "zone_end": latest["end"],
        "gap_size": latest["size"]
    }

def get_fvg_distance_percent(
    current_price,
    fvg
):

    if not fvg:
        return 999

    midpoint = (
        fvg["start"]
        + fvg["end"]
    ) / 2

    distance = abs(
        current_price
        - midpoint
    )

    percent = (
        distance
        / current_price
    ) * 100

    return percent
