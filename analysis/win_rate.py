import pandas as pd

df = pd.read_csv("signals_log.csv")
df["win"] = df["price_change_pct"] > 0

summary = df.groupby("confidence").agg(
    total=("win", "count"),
    win_rate=("win", "mean")
)

summary["win_rate"] = (summary["win_rate"] * 100).round(2)
print(summary)
