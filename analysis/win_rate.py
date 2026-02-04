import pandas as pd
import yfinance as yf

LOOKAHEAD = 5

def future_return(ticker, date):
    df = yf.download(ticker, period="1mo", progress=False)
    df.index = pd.to_datetime(df.index)

    date = pd.to_datetime(date)
    future = df[df.index > date].head(LOOKAHEAD)

    if future.empty:
        return None

    entry = df[df.index <= date].iloc[-1]["Close"]
    exit = future.iloc[-1]["Close"]

    return (exit-entry)/entry*100


def analyze(csv="data/signals_log.csv"):
    df = pd.read_csv(csv)
    rows = []

    for _, r in df.iterrows():
        ret = future_return(r["ticker"], r["date"])
        if ret is None:
            continue

        for reason in r["reason"].split(" + "):
            rows.append({
                "reason": reason,
                "win": ret > 0,
                "return": ret
            })

    res = pd.DataFrame(rows)
    return (
        res.groupby("reason")
        .agg(
            trades=("win","count"),
            win_rate=("win","mean"),
            avg_return=("return","mean")
        )
        .assign(win_rate=lambda x: x.win_rate*100)
        .sort_values("win_rate",ascending=False)
    )

if __name__ == "__main__":
    print(analyze())
