from groq import Groq
from config.settings import GROQ_API_KEY

# Create Groq client
client = Groq(api_key=GROQ_API_KEY)

class NarratorAgent:
    def run(self, s):
        """
        s: dict with keys:
            ticker
            price_change_pct
            volume_ratio
            confidence
            news (list of dict) — optional
        """

        # Build news section if exists
        news_block = ""
        if s.get("news"):
            for i, n in enumerate(s["news"]):
                title = n.get("title", "").strip()
                published = n.get("published", "").strip()
                link = n.get("link", "").strip()
                news_block += f"{i+1}. {title} ({published})\n{link}\n\n"

        # Build the prompt
        prompt = f"""
You are an Indonesian stock market analyst (IDX).
Create a concise insight (maximum 2 sentences). Focus on the quantitative change,
and only mention the news if it clearly explains the stock's movement.

Ticker: {s['ticker']}
Price Change: {s['price_change_pct']}%
Volume Ratio: {s['volume_ratio']}
Confidence Level: {s['confidence']}

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
