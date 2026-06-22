from detectors.bos import detect_bos
from detectors.choch import detect_choch
from detectors.fvg import detect_fvg


# =========================
# TREND
# =========================
def get_trend(h1_df):

    if len(h1_df) < 50:
        return None

    close = h1_df["close"]

    ema20 = close.ewm(span=20).mean().iloc[-1]
    ema50 = close.ewm(span=50).mean().iloc[-1]

    if ema20 > ema50:
        return "bullish"

    if ema20 < ema50:
        return "bearish"

    return None


# =========================
# VALIDATE SIGNAL
# =========================
def validate_signal(symbol, h1_df, m15_df):

    trend = get_trend(h1_df)

    if trend is None:
        return None

    bos = detect_bos(m15_df)
    choch = detect_choch(m15_df)
    fvg = detect_fvg(m15_df)

    if not bos or not choch or not fvg:
        return None

    current_price = float(m15_df["close"].iloc[-1])

    # BUY SETUP
    if (
        trend == "bullish"
        and bos.get("direction") == "bullish"
        and choch.get("direction") == "bullish"
        and fvg.get("type") == "bullish"
    ):

        return {
            "symbol": symbol,
            "side": "BUY",
            "trend": trend,
            "bos": bos,
            "choch": choch,
            "fvg": fvg,
            "current_price": current_price
        }

    # SELL SETUP
    if (
        trend == "bearish"
        and bos.get("direction") == "bearish"
        and choch.get("direction") == "bearish"
        and fvg.get("type") == "bearish"
    ):

        return {
            "symbol": symbol,
            "side": "SELL",
            "trend": trend,
            "bos": bos,
            "choch": choch,
            "fvg": fvg,
            "current_price": current_price
        }

    return None


# =========================
# MESSAGE BUILDER
# =========================
def build_signal_message(signal):

    side = signal.get("side")
    symbol = signal.get("symbol")

    bos = signal.get("bos", {})
    choch = signal.get("choch", {})
    fvg = signal.get("fvg", {})

    current_price = signal.get("current_price", 0)

    emoji = "🟢" if side == "BUY" else "🔴"

    message = f"""
{emoji} SMC SIGNAL

Symbol: {symbol}
Side: {side}

Trend Structure:
BOS: {bos.get('direction', 'N/A')}
CHoCH: {choch.get('direction', 'N/A')}

FVG:
Type: {fvg.get('type', 'N/A')}
Zone: {round(fvg.get('start', 0), 6)} - {round(fvg.get('end', 0), 6)}

Current Price:
{round(current_price, 6)}
"""

    return message.strip()
