import feedparser

class NewsAgent:
    def run(self, ticker):
        query = f"{ticker} saham Indonesia"
        url = f"https://news.google.com/rss/search?q={query}"

        feed = feedparser.parse(url)
        items = feed.get("entries", [])

        if not items:
            return None

        # Ambil 3 berita terbaru
        top3 = items[:3]

        # Format
        news_list = []
        for item in top3:
            news_list.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "published": item.get("published"),
                "summary": item.get("summary", "")
            })

        return news_list
