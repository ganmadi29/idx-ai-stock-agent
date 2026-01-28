import yfinance as yf

def get_stock_data(ticker, period="7d"):
    df = yf.Ticker(ticker).history(period=period)
    df = df.reset_index()
    df["ticker"] = ticker
    return df
