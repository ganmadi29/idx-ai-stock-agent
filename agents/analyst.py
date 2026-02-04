import pandas as pd
import numpy as np
from tools.indicators import rsi

class AnalystAgent:
    def analyze(self, df: pd.DataFrame):

        # ✅ FIX: flatten MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # safety check
        if len(df) < 55:
            return None

        close = df["Close"].iloc[-1]
        prev_close = df["Close"].iloc[-2]
        volume = df["Volume"].iloc[-1]
        vol_avg = df["Volume"].rolling(20).mean().iloc[-1]
        vol_ratio = volume / vol_avg if vol_avg > 0 else 0

        # =====================
        # MOVING AVERAGES
        # =====================
        ma20 = df["Close"].rolling(20).mean().iloc[-1]
        ma50 = df["Close"].rolling(50).mean().iloc[-1]

        # =====================
        # RSI
        # =====================
        delta = df["Close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        rs = gain.rolling(14).mean() / loss.rolling(14).mean()
        rsi = 100 - (100 / (1 + rs))
        rsi_val = rsi.iloc[-1]

        # =====================
        # PRICE CHANGE
        # =====================
        change_pct = ((close - prev_close) / prev_close) * 100

        # =====================
        # REASONS
        # =====================
        reasons = []

        if vol_ratio >= 2:
            reasons.append(f"Vx{round(vol_ratio,1)}")

        if rsi_val >= 50:
            reasons.append("RSI_OK")

        if close > ma20:
            reasons.append("MA20_OK")

        if ma20 > ma50:
            reasons.append("MA_TREND")

        if close > ma50:
            reasons.append("STRONG_TREND")

        if not reasons:
            return None

        # =====================
        # SCORE
        # =====================
        score = (
            change_pct
            * vol_ratio
            * (rsi_val / 50)
        )

        # Trend bonus
        if ma20 > ma50:
            score *= 1.2

        # Weak trend penalty
        if close < ma20:
            score *= 0.8

        # =====================
        # CONFIDENCE
        # =====================
        confidence = "LOW"
        if "MA_TREND" in reasons and vol_ratio >= 2:
            confidence = "HIGH"
        elif vol_ratio >= 1.5:
            confidence = "MEDIUM"

        return {
            "ticker": df.attrs["ticker"],
            "price": round(close, 2),
            "change_pct": round(change_pct, 2),
            "vol_ratio": round(vol_ratio, 2),
            "rsi": round(rsi_val, 1),
            "ma20": round(ma20, 2),
            "ma50": round(ma50, 2),
            "reasons": reasons,
            "reason": " + ".join(reasons),
            "score": round(score, 2),
            "confidence": confidence
        }
