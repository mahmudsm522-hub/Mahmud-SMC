import requests
import pandas as pd

from config.settings import (
    BYBIT_BASE_URL,
    TIMEFRAME,
    CANDLE_LIMIT
)


def get_klines(symbol):

    url = f"{BYBIT_BASE_URL}/v5/market/kline"

    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": TIMEFRAME,
        "limit": CANDLE_LIMIT
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    data = response.json()

    if data["retCode"] != 0:
        raise Exception(data)

    candles = data["result"]["list"]

    rows = []

    for c in candles:

        rows.append({
            "timestamp": int(c[0]),
            "open": float(c[1]),
            "high": float(c[2]),
            "low": float(c[3]),
            "close": float(c[4]),
            "volume": float(c[5])
        })

    df = pd.DataFrame(rows)

    df = df.sort_values("timestamp")

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df
