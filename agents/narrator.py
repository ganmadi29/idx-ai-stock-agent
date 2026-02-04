from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

class NarratorAgent:
    def run(self, signal):
        prompt = f"""
You are an Indonesian stock market analyst (IDX).
Create a concise insight (max 2 sentences).

Ticker: {signal['ticker']}
Price: {signal['price']}
Volume Ratio: {signal['volume_ratio']}
RSI: {signal['rsi']}
Reason: {signal['reason']}
Score: {signal['score']}
"""
        r = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # model aktif & stabil
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return r.choices[0].message.content.strip()
