import requests
import pandas as pd

BASE_URL = "https://api.bybit.com"


def get_symbols():

    url = (
        f"{BASE_URL}"
        "/v5/market/instruments-info"
    )

    params = {
        "category": "linear"
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    data = response.json()

    if data["retCode"] != 0:
        raise Exception(data)

    symbols = []

    for item in data["result"]["list"]:

        symbol = item["symbol"]

        status = item.get(
            "status",
            ""
        )

        if (
            symbol.endswith("USDT")
            and
            status == "Trading"
        ):

            symbols.append(symbol)

    return sorted(symbols)


def get_klines(
    symbol,
    interval="15",
    limit=200
):

    url = (
        f"{BASE_URL}"
        "/v5/market/kline"
    )

    params = {
        "category": "linear",
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
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

    df = df.sort_values(
        "timestamp"
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df
