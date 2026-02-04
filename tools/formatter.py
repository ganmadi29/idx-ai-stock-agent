def format_signal_message(signal: dict) -> str:
    reasons = "\n".join(f"• {r}" for r in signal["reasons"])

    return f"""
📈 <b>{signal['ticker']}</b>

<b>Price</b>   : {signal['price']} ({signal['price_change']})
<b>Volume</b>  : {signal['volume_ratio']}x avg
<b>Signal</b>  : <b>{signal['signal']}</b>
<b>Score</b>   : {signal['score']} / 5

<b>Reason</b>
{reasons}

<b>Insight</b>
{signal['insight']}
""".strip()
