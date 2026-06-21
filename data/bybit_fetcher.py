symbolsst_symbols():

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

        data = response.json()

        if data["retCode"] != 0:
            raise Exception(data)

        result = data["result"]

        for item in result["list"]:

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

        cursor = result.get(
            "nextPageCursor",
            ""
        )

        if not cursor:
            break

    symbols = sorted(
        list(set(symbols))
    )

    return symboldef get_top_symbols_by_volume(limit=100):

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

        if not symbol.endswith(
            "USDT"
        ):
            continue

        try:

            turnover = float(
                item.get(
                    "turnover24h",
                    0
                )
            )

        except Exception:

            turnover = 0

        tickers.append(
            {
                "symbol": symbol,
                "turnover": turnover
            }
        )

    tickers.sort(
        key=lambda x:
        x["turnover"],
        reverse=True
    )

    return [
        x["symbol"]
        for x in tickers[:limit]
        ]s
