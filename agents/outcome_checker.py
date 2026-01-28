from tools.market_api import get_stock_data

class OutcomeCheckerAgent:
    def run(self, ticker, entry_price):
        df = get_stock_data(ticker, "5d")
        future_price = df.iloc[-1]["Close"]
        return round((future_price - entry_price) / entry_price * 100, 2)
