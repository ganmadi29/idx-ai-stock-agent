import yfinance as yf
from tools.watchlist import load_watchlist
from agents.analyst import AnalystAgent
from agents.narrator import NarratorAgent
from tools.telegram import send_telegram
from tools.formatter import format_signal_message

def main():
    watchlist = load_watchlist()
    analyst = AnalystAgent()
    narrator = NarratorAgent()

    signals = []

    for _, row in watchlist.iterrows():
        if not row["enabled"]:
            continue

        ticker = row["ticker"]
        lookback = int(row["lookback"])
        vol_mult = float(row["vol_mult"])

        df = yf.download(ticker, period="4mo", progress=False)

        if df.empty:
            continue

        signal = analyst.analyze(df)

        if signal:
            signal["ticker"] = ticker
            signal["lookback"] = lookback
            signal["vol_mult"] = vol_mult
            signal["insight"] = narrator.run(signal)
            signals.append(signal)

    if not signals:
        send_telegram("📭 No signal today.")
        return

    send_telegram(
        "🚀 <b>IDX Daily Breakout Signals</b>\n"
        "Scan completed.\n")
    
    for signal in signals:
        
        message = format_signal_message(signal)
        send_telegram(message)



if __name__ == "__main__":
    main()
