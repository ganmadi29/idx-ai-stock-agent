from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

class NarratorAgent:
    def run(self, signal):
        prompt = f"""
You are a professional swing trader and equity research analyst. (IDX).
Create a concise insight (max 3 sentences).
Time horizon: Swing trade (5–30 trading days)
Risk profile: Medium risk

1. TECHNICAL ANALYSIS

Identify the current trend using:
- Market structure (HH, HL, LH, LL)
- 20 / 50 MA

Analyze momentum using:
- RSI (divergence if any)

Identify key levels:
- Major support & resistance
- Volume profile / high volume nodes

Candlestick confirmation:
- Recent reversal or continuation patterns

Volatility check:
- ATR and recent range behavior

Important rules:

Be objective, not bullish by default
Clearly state if NO TRADE is the best decision
Focus on probabilities, not certainty
And no SHORT Recommendation only SPOT

Ticker: {signal['ticker']}
Price: {signal['price']}
Price Change: {signal['change_pct']}%
Volume Ratio: {signal['volume_ratio']}
RSI: {signal['rsi']}
MA20: {signal['ma20']}
MA50: {signal['ma50']}
Confidence: {signal['confidence']}
Reason: {signal['reason']}
Score: {signal['score']}
"""
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # model aktif & stabil
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return r.choices[0].message.content.strip()
