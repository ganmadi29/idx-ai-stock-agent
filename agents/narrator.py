from groq import Groq
from config.settings import GROQ_API_KEY

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)

class NarratorAgent:
    def run(self, ticker, signal):
        news = NewsAgent().get_news(ticker)

        prompt = f"""
You are a stock market analyst.
Explain this signal in clear, short Indonesian.

Ticker: {ticker}
Price: {signal['price']}
Reason: {signal['reason']}
RSI: {signal['rsi']}
Volume Ratio: {signal['volume_ratio']}

Recent News:
{news}

Explain:
- What happened technically
- Why it matters
- Short risk reminder
"""

        if news_block:
            prompt += "Latest News:\n" + news_block

        prompt += "\nInsight:"

        # If API key is missing, return fallback text
        if not GROQ_API_KEY:
            return "Insight AI unavailable (GROQ API key missing)."

        # Generate completion
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=120
            )

            result = response.choices[0].message.content.strip()
            return result

        except Exception as e:
            # Fallback if something goes wrong
            print("NarratorAgent error:", e)
            return "Insight AI unavailable (model error)."
