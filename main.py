from data.bybit_fetcher import get_klines

def main():

    symbol = "BTCUSDT"

    df = get_klines(symbol)

    print(df.tail())

    print()
    print(f"{symbol} loaded")
    print(f"Candles: {len(df)}")

if __name__ == "__main__":
    main()
