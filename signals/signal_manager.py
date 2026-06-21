from detectors.bos import detect_bos
from detectors.choch import detect_choch
from detectors.fvg import detect_fvg


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


def validate_signal(
    symbol,
    h1_df,
    m15_df
):

    trend = get_trend(h1_df)

    if trend is None:
        return None

    bos = detect_bos(m15_df)
    choch = detect_choch(m15_df)
    fvg = detect_fvg(m15_df)

    if not bos:
        return None

    if not choch:
        return None

    if not fvg:
        return None

    # BUY SETUP

    if (
        trend == "bullish"
        and
        bos["direction"] == "bullish"
        and
        choch["direction"] == "bullish"
        and
        fvg["type"] == "bullish"
    ):

        return {
            "symbol": symbol,
            "side": "BUY",
            "trend": trend,
            "bos": bos,
            "choch": choch,
            "fvg": fvg
        }

    # SELL SETUP

    if (
        trend == "bearish"
        and
        bos["direction"] == "bearish"
        and
        choch["direction"] == "bearish"
        and
        fvg["type"] == "bearish"
    ):

        return {
            "symbol": symbol,
            "side": "SELL",
            "trend": trend,
            "bos": bos,
            "choch": choch,
            "fvg": fvg
        }

    return None


def build_signal_message(signal):

    side = signal["side"]
    symbol = signal["symbol"]

    bos = signal["bos"]
    choch = signal["choch"]
    fvg = signal["fvg"]

    emoji = "🟢" if side == "BUY" else "🔴"

    message = f"""
{emoji} SMC SIGNAL

Symbol: {symbol}

Side: {side}

BOS:
{bos['direction']}

CHoCH:
{choch['direction']}

FVG:
{fvg['type']}

Zone:
{round(fvg['start'], 6)}
-
{round(fvg['end'], 6)}
"""

    return message.strip()
