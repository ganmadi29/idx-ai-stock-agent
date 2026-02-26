import yfinance as yf
import json
from tools.watchlist import load_watchlist
from agents.analyst import AnalystAgent
from agents.narrator import NarratorAgent
from tools.telegram import send_telegram
from tools.formatter import format_signal_message
import gspread
from google.oauth2.service_account import Credentials

# =============================
# GOOGLE SHEETS INIT
# =============================
SPREADSHEET_ID = "1oBUHkoXJ95pMeJAf3k5FXxHQQJFbx8rt5ebyg0tTbQg"
WORKSHEET_NAME = "watchlist"
LOG_SHEET = "AI_log"

def get_gspread_client():
    creds = Credentials.from_service_account_info(
        json.loads(os.environ["GCP_SA_KEY"]),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return gspread.authorize(creds)



# =============================
# LOG SIGNALS
# =============================

def log_signals(gc, signals):
    if not signals:
        return

    ws = gc.open_by_key(SPREADSHEET_ID).worksheet(LOG_SHEET)
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = []
    for s in signals:
        rows.append([
            today,
            s.get("ticker"),
            s.get("price"),
            s.get("change"),
            s.get("volume_ratio"),
            s.get("rsi"),
            s.get("fundamental"),
            ", ".join(s.get("reasons", [])),
            s.get("score"),
            s.get("confidence")
        ])

    ws.append_rows(rows, value_input_option="USER_ENTERED")



def main():
    gc = get_gspread_client()
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
            
        df.attrs["ticker"] = ticker
        signal = analyst.analyze(df)

        if signal:
            signal["ticker"] = ticker
            signal["lookback"] = lookback
            signal["vol_mult"] = vol_mult
            signal["insight"] = narrator.run(signal)
            signals.append(signal)
            
    signals = [
        s for s in signals
        if s["confidence"] == "HIGH"
        and "MA_TREND" in s["reasons"]
        and s["volume_ratio"] >= 2
    ]
    
    signals = sorted(signals, key=lambda x: x["score"], reverse=True)
    signals = signals[:10]
    
    if not signals:
        send_telegram("📭 No signal today.")
        return

    send_telegram(
        "🚀 <b>IDX Daily Breakout Signals</b>\n"
        "Scan completed.\n")

    log_signals(gc, signals)
    
    for signal in signals:
        
        message = format_signal_message(signal)
        send_telegram(message)



if __name__ == "__main__":
    main()
