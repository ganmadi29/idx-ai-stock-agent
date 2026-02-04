import yfinance as yf
from agents.analyst import AnalystAgent
from agents.narrator import NarratorAgent
import pandas as pd
from datetime import datetime

WATCHLIST = ["BBCA.JK","BMRI.JK","ADRO.JK"]

analyst = AnalystAgent()
narrator = NarratorAgent()

logs = []

for t in WATCHLIST:
    df = yf.download(t, period="6mo", progress=False)
    if df.empty:
        continue

    signal = analyst.analyze(df)
    if not signal:
        continue

    insight = narrator.run(t, signal)
    print(f"\n🔥 {t}\n{insight}")

    logs.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "ticker": t,
        "reason": signal["reason"],
        "price": signal["price"]
    })

if logs:
    pd.DataFrame(logs).to_csv("data/signals_log.csv",mode="a",index=False,header=False)
