from groq import Groq
from config.settings import GROQ_API_KEY

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
        price_vs_ma20 = "above" if close > ma20 else "below"
        rsi_state = "overbought" if rsi >= 70 else ("oversold" if rsi <= 30 else "neutral")

        news_section = f"\nRecent News:\n{signal.get('news', 'No recent news.')}\n" if signal.get('news') else ""

        prompt = f"""You are a quantitative analyst reviewing a momentum signal for an IDX swing trade candidate.
Analyze ONLY the data provided. Do not invent price history, support/resistance levels, candlestick patterns, or ATR values not derivable from these numbers.

Data:
- Ticker: {signal['ticker']}
- Price: {close} ({change_pct:+.2f}% today)
- Volume: {vol_ratio}x average (high volume confirmation)
- RSI(14): {rsi} — {rsi_state}
- MA20: {ma20} | MA50: {ma50} — {trend} trend structure
- Price is {price_vs_ma20} MA20
- Signal score: {signal['score']} | Confidence: {signal['confidence']}
- Triggers: {signal['reason']}{news_section}

Write exactly 3 sentences:
1. Describe the trend and momentum based strictly on MA and RSI values above.
2. Assess volume conviction and what the {change_pct:+.2f}% move with {vol_ratio}x volume implies.
3. State the trading implication (entry consideration or "NO TRADE" if the setup is ambiguous). No short recommendations — spot only.

Be objective. Do not invent data."""

        try:
            r = self._client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200,
            )
            return r.choices[0].message.content.strip()
        except Exception as e:
            print(f"[NarratorAgent] API error for {signal.get('ticker')}: {e}")
            return "AI insight unavailable."
