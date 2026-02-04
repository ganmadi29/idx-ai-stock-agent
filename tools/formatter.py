def format_signal_message(signal):
    return (
        f"🔥 <b>{signal['ticker']}</b>\n"
        f"Price: {signal['price']} ({signal['change_pct']}%)\n"
        f"MA20 / MA50: {signal['ma20']} / {signal['ma50']}\n"
        f"Confidence: <b>{signal['confidence']}</b>\n"
        f"Score: <b>{signal['score']:.2f}</b>\n\n"
        f"Reason:\n"
        f"• {signal['reason']}\n\n"
        f"Insight:\n"
        f"{signal['insight']}"
    )
