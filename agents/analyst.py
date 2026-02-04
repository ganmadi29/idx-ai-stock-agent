import pandas as pd
from tools.indicators import rsi

class AnalystAgent:
    def analyze(self, df: pd.DataFrame):

        # ✅ FIX: flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # safety check
        if len(df) < 25:
            return None

        latest = df.iloc[-1]

        high_20 = df["High"].rolling(20).max().iloc[-2]
        high_10 = df["High"].rolling(10).max().iloc[-2]
        vol_avg = df["Volume"].rolling(20).mean().iloc[-2]

        # ✅ FORCE scalar
        close_price = float(latest["Close"])
        volume = float(latest["Volume"])

        reasons = []

        if close_price > high_20:
            reasons.append("B20DH")
        elif close_price > high_10:
            reasons.append("B10DH")

        vol_ratio = volume / vol_avg
        if vol_ratio > 2:
            reasons.append(f"Vx{round(vol_ratio,1)}")

        rsi_val = float(rsi(df["Close"]).iloc[-1])
        if rsi_val < 70:
            reasons.append("RSI_OK")

        score = len(reasons)

        if score >= 2:
            return {
                "price": round(close_price, 2),
                "change_pct": round(df["Close"].pct_change().iloc[-1] * 100, 2),
                "volume_ratio": round(vol_ratio, 2),
                "rsi": round(rsi_val, 1),
                "reason": " + ".join(reasons),
                "score": score
            }

        return None
