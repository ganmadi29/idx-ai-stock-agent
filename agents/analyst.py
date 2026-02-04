import pandas as pd
from tools.indicators import rsi

class AnalystAgent:
    def analyze(self, df: pd.DataFrame):
        latest = df.iloc[-1]
        high_20 = df["High"].rolling(20).max().iloc[-2]
        high_10 = df["High"].rolling(10).max().iloc[-2]
        vol_avg = df["Volume"].rolling(20).mean().iloc[-2]

        reasons = []

        if latest["Close"] > high_20:
            reasons.append("B20DH")
        elif latest["Close"] > high_10:
            reasons.append("B10DH")

        if latest["Volume"] > vol_avg * 2:
            reasons.append(f"Vx{round(latest['Volume']/vol_avg,1)}")

        rsi_val = rsi(df["Close"]).iloc[-1]
        if rsi_val < 70:
            reasons.append("RSI_OK")

        score = len(reasons)

        if score >= 2:
            return {
                "price": latest["Close"],
                "volume_ratio": round(latest["Volume"]/vol_avg,2),
                "rsi": round(rsi_val,1),
                "reason": " + ".join(reasons),
                "score": score
            }

        return None
