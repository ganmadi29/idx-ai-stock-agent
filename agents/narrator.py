from groq import Groq
from config.settings import GROQ_API_KEY

_TRIGGER_LABELS = {
    "MA_TREND":     "MA20 > MA50 (uptrend confirmed)",
    "MA20_OK":      "Price above MA20",
    "RSI_OK":       "RSI above neutral (50)",
    "STRONG_TREND": "Price above MA50 (strong trend)",
}

class NarratorAgent:
    def __init__(self):
        self._client = Groq(api_key=GROQ_API_KEY)

    def run(self, signal):
        ma20 = signal['ma20']
        ma50 = signal['ma50']
        close = signal['price']
        rsi = signal['rsi']
        vol_ratio = signal['volume_ratio']
        change_pct = signal['change_pct']

        trend = "bullish" if ma20 > ma50 else "bearish"
        rsi_state = "overbought" if rsi >= 70 else ("oversold" if rsi <= 30 else "neutral")
        ma20_dist = round(((close - ma20) / ma20) * 100, 2)

        readable_triggers = "\n".join(
            f"  • {_TRIGGER_LABELS.get(r, r)}"
            for r in signal.get('reasons', [])
            if not r.startswith('Vx')  # volume already shown in data
        )

        news_section = (
            f"\nRecent News:\n{signal['news']}\n"
            if signal.get('news') and signal['news'] != "No recent news."
            else ""
        )

        system_msg = (
            "You are a quantitative analyst specializing in the Indonesian Stock Exchange (IDX). "
            "IDX is retail-driven with T+2 settlement and auto-rejection (ARB) limits. "
            "Be objective and data-driven. Never invent price levels, patterns, or figures "
            "not explicitly given to you."
        )

        user_msg = f"""Review this IDX momentum signal:

Ticker: {signal['ticker']}
Price: {close} ({change_pct:+.2f}% today, {ma20_dist:+.2f}% above MA20)
Volume: {vol_ratio}x 20-day average
RSI(14): {rsi} ({rsi_state})
Trend: MA20 {ma20} vs MA50 {ma50} → {trend}{news_section}

Signal triggers:
{readable_triggers}

Write 2-3 sentences covering: trend strength, what the volume and price move implies, and whether this is an actionable spot entry or NO TRADE. No short recommendations."""

        try:
            r = self._client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.3,
                max_tokens=300,
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            print(f"[NarratorAgent] API error for {signal.get('ticker')}: {e}")
            return "AI insight unavailable."
