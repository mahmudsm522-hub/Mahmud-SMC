import pandas as pd


def find_swing_highs(df, lookback=3):

    swings = []

    highs = df["high"].tolist()

    for i in range(
        lookback,
        len(highs) - lookback
    ):

        current = highs[i]

        left = highs[
            i - lookback:i
        ]

        right = highs[
            i + 1:i + lookback + 1
        ]

        if (
            current > max(left)
            and
            current > max(right)
        ):

            swings.append(
                {
                    "index": i,
                    "price": current
                }
            )

    return swings


def find_swing_lows(df, lookback=3):

    swings = []

    lows = df["low"].tolist()

    for i in range(
        lookback,
        len(lows) - lookback
    ):

        current = lows[i]

        left = lows[
            i - lookback:i
        ]

        right = lows[
            i + 1:i + lookback + 1
        ]

        if (
            current < min(left)
            and
            current < min(right)
        ):

            swings.append(
                {
                    "index": i,
                    "price": current
                }
            )

    return swings


def get_last_swing_high(df):

    highs = find_swing_highs(df)

    if not highs:
        return None

    return highs[-1]


def get_last_swing_low(df):

    lows = find_swing_lows(df)

    if not lows:
        return None

    return lows[-1]


def get_market_structure(df):

    swing_high = get_last_swing_high(df)

    swing_low = get_last_swing_low(df)

    return {
        "swing_high": swing_high,
        "swing_low": swing_low
    }
