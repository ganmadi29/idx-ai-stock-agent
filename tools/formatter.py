def format_signal_message(signal):
    return (
        f"🔥 <b>{signal['ticker']}</b>\n"
        f"Price: {signal['price']} ({signal['change_pct']}%)\n"
        f"Score: <b>{signal['score']:.2f}</b>\n\n"
        f"Reason:\n"
        f"• {signal['reason']}\n\n"
        f"Insight:\n"
        f"{signal['insight']}"
    )
