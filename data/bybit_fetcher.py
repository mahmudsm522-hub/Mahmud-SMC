import requests
import pandas as pd

BASE_URL = "https://api.bybit.com"


# =========================
# GET ALL USDT SYMBOLS
# =========================
def get_symbols():

    symbols = []
    cursor = ""

    while True:

        url = (
            f"{BASE_URL}"
            "/v5/market/instruments-info"
        )

        params = {
            "category": "linear",
            "limit": 1000
        }

        if cursor:
            params["cursor"] = cursor

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        print("Status:", response.status_code)
print("Response:", response.text[:1000])

data = response.json()

        if data["retCode"] != 0:
            raise Exception(data)

        result = data["result"]

        for item in result["list"]:

            symbol = item["symbol"]
            status = item.get("status", "")

            if (
                symbol.endswith("USDT")
                and status == "Trading"
            ):
                symbols.append(symbol)

        cursor = result.get("nextPageCursor", "")

        if not cursor:
            break

    return sorted(list(set(symbols)))


# =========================
# TOP VOLUME SYMBOLS
# =========================
def get_top_symbols_by_volume(limit=100):

    url = (
        f"{BASE_URL}"
        "/v5/market/tickers"
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

    tickers = []

    for item in data["result"]["list"]:

        symbol = item["symbol"]

        if not symbol.endswith("USDT"):
            continue

        try:
            turnover = float(
                item.get("turnover24h", 0)
            )
        except Exception:
            turnover = 0

        tickers.append({
            "symbol": symbol,
            "turnover": turnover
        })

    tickers.sort(
        key=lambda x: x["turnover"],
        reverse=True
    )

    return [
        x["symbol"]
        for x in tickers[:limit]
    ]


# =========================
# KLINES / CANDLES
# =========================
def get_klines(symbol, interval="15", limit=200):

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

    df = df.sort_values("timestamp")
    df.reset_index(drop=True, inplace=True)

    return df
