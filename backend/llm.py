from backend.config import LLM_PROVIDER

def detect_intent(text: str) -> str:
    t = (text or "").lower()

    if any(k in t for k in ["bullish", "bearish", "trend", "direction"]):
        return "trend"

    if any(k in t for k in ["buy", "sell", "wait", "entry", "exit", "should i"]):
        return "decision"

    if any(k in t for k in ["rsi", "relative strength"]):
        return "explain_rsi"

    if any(k in t for k in ["sma", "moving average", "ma ", "ma?"]):
        return "explain_ma"

    if any(k in t for k in ["forecast", "predict", "prediction", "next", "7 days", "tomorrow"]):
        return "forecast"

    return "summary"


def generate_reply(user_msg: str, context: dict) -> str:
    """
    context must contain:
      asset, horizon, last_value, last_date, rsi_14, sma_14, sma_50, trend, next_end
    """
    # If later you add a real LLM provider, you can switch here
    if LLM_PROVIDER != "mock":
        raise NotImplementedError("Set LLM_PROVIDER and implement provider client.")

    intent = detect_intent(user_msg)

    asset = context["asset"]
    horizon = context["horizon"]
    last_value = context["last_value"]
    last_date = context["last_date"]
    rsi_14 = context["rsi_14"]
    sma_14 = context["sma_14"]
    sma_50 = context["sma_50"]
    trend = context["trend"]
    next_end = context["next_end"]

    if intent == "trend":
        bias = "above" if (sma_50 is not None and sma_14 > sma_50) else "below"
        return (
            f"**Trend for {asset}: {trend}**\n\n"
            f"- Last close: **{last_value:,.2f}** (as of {last_date})\n"
            f"- RSI(14): **{rsi_14:,.2f}**\n"
            f"- SMA(14): **{sma_14:,.2f}**\n"
            + (f"- SMA(50): **{sma_50:,.2f}** (SMA14 is {bias} SMA50)\n" if sma_50 is not None else "")
            + (f"\nModel forecast (end of {horizon} days): **{float(next_end):,.2f}**\n" if next_end is not None else "")
        )

    if intent == "decision":
        # very simple rule-of-thumb (NOT financial advice)
        if rsi_14 < 40:
            suggestion = "Potentially **BUY/ACCUMULATE** (RSI is relatively low)."
        elif rsi_14 > 70:
            suggestion = "⚠️ **CAUTION / WAIT** (RSI is high; could be overbought)."
        else:
            suggestion = "**WAIT / DCA** (RSI is mid-range; confirm with trend)."

        return (
            f"**{asset}: Buy or wait? (rule-of-thumb)**\n\n"
            f"- Trend: **{trend}**\n"
            f"- RSI(14): **{rsi_14:,.2f}**\n"
            + (f"- Forecast end ({horizon} days): **{float(next_end):,.2f}**\n" if next_end is not None else "")
            + f"\n➡️ Suggestion: {suggestion}\n\n"
            "Tell me your risk level (**low/medium/high**) and I’ll tailor it."
        )

    if intent == "explain_rsi":
        return (
            "**RSI explained (simple):**\n"
            "- RSI ranges 0–100 and measures momentum.\n"
            "- Above ~70 = overbought (price ran up fast)\n"
            "- Below ~30 = oversold (price dropped fast)\n\n"
            f"For **{asset}**, RSI(14) is **{rsi_14:,.2f}** right now → trend bias: **{trend}**."
        )

    if intent == "explain_ma":
        return (
            "**Moving averages (SMA) explained:**\n"
            "- SMA(14) tracks short-term direction.\n"
            "- SMA(50) tracks medium-term direction.\n"
            "- If SMA(14) > SMA(50): bullish bias. If below: bearish/neutral.\n\n"
            f"For **{asset}**:\n"
            f"- SMA(14): **{sma_14:,.2f}**\n"
            + (f"- SMA(50): **{sma_50:,.2f}**\n" if sma_50 is not None else "")
            + f"- Bias: **{trend}**"
        )

    if intent == "forecast":
        return (
            f"**Forecast for {asset} (next {horizon} days)**\n\n"
            f"- Last close: **{last_value:,.2f}** (as of {last_date})\n"
            + (f"- Expected level near **{float(next_end):,.2f}** by end of horizon\n" if next_end is not None else "")
            + "\nIf you want: I can list the predicted values day-by-day."
        )

    # summary fallback
    out = (
        f"**{asset} summary**\n\n"
        f"- Last close: **{last_value:,.2f}** (as of {last_date})\n"
        f"- RSI(14): **{rsi_14:,.2f}**\n"
        f"- SMA(14): **{sma_14:,.2f}**\n"
    )
    if sma_50 is not None:
        out += f"- SMA(50): **{sma_50:,.2f}** → Trend: **{trend}**\n"
    if next_end is not None:
        out += f"\n**Forecast (end of {horizon} days):** **{float(next_end):,.2f}**\n"
    out += "\nAsk: *bullish/bearish?*, *buy or wait?*, *explain RSI*, *forecast next 7 days*."
    return out