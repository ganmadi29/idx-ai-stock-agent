class AnalystAgent:
    def run(self, df):
        if len(df) < 5:
            return None

        last = df.iloc[-1]
        prev = df.iloc[-2]

        avg_vol = df["Volume"].tail(5).mean()
        price_change = (last["Close"] - prev["Close"]) / prev["Close"]
        volume_ratio = last["Volume"] / avg_vol

        if price_change > 0.03 and volume_ratio > 1.5:
            return {
                "ticker": last["ticker"],
                "signal_price": round(last["Close"], 2),
                "price_change_pct": round(price_change * 100, 2),
                "volume_ratio": round(volume_ratio, 2)
            }
