from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

class NarratorAgent:
    def run(self, s):
        news_block = ""
        if s.get("news"):
            news_block = f"""
Recent News:
Headline: {s['news']['headline']}
Summary: {s['news']['summary']}
"""

        prompt = f"""
You are an Indonesian stock market analyst (IDX).
Create a concise insight (max 2 sentences).
Mention news ONLY if relevant to price/volume movement.

Ticker: {s['ticker']}
Price Change: {s['price_change_pct']}%
Volume Ratio: {s['volume_ratio']}
Confidence: {s['confidence']}
{news_block}
"""
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=120
        )
        return r.choices[0].message.content.strip()
