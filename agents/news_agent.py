import feedparser
from urllib.parse import quote_plus

class NewsAgent:
    def run(self, ticker):
        # Build query safely
        query = f"{ticker} saham Indonesia"
        encoded_query = quote_plus(query)

        url = f"https://news.google.com/rss/search?q={encoded_query}"

        feed = feedparser.parse(url)
        entries = feed.get("entries", [])

        if not entries:
            return None

        news_list = []
        for item in entries[:3]:  # ambil 3 terbaru
            news_list.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "published": item.get("published", ""),
                "summary": item.get("summary", "")
            })

        return news_list
