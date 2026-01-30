from datetime import datetime
from config.idx_tickers import IDX_TICKERS
from agents.analyst import AnalystAgent
from agents.validator import ValidatorAgent
from agents.narrator import NarratorAgent
from tools.market_api import get_stock_data
from tools.storage import save_signal
from tools.telegram import send_telegram_message
from agents.news_agent import NewsAgent

def main():
    analyst = AnalystAgent()
    validator = ValidatorAgent()
    narrator = NarratorAgent()
    news_agent = NewsAgent()

    today = datetime.utcnow().strftime("%Y-%m-%d")

    for ticker in IDX_TICKERS:
        df = get_stock_data(ticker)
        base = analyst.run(df)
        if not base:
            continue

        news = news_agent.run(ticker)
        base["news"] = news
        
        valid = validator.run(base)
        if not valid:
            continue

        insight = narrator.run(valid)

        record = {
            "date": today,
            **valid,
            "insight": insight
        }

        save_signal(record)

        msg = f"""
📈 IDX SIGNAL

{valid['ticker']}
Price: {valid['signal_price']}
Change: {valid['price_change_pct']}%
Volume Ratio: {valid['volume_ratio']}
Confidence: {valid['confidence']}

🧠 {insight}
"""
        send_telegram_message(msg)

if __name__ == "__main__":
    main()
