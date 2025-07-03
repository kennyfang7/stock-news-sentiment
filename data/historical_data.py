import yfinance as yf
import pandas as pd

def fetch_stock_history(ticker: str, period: str = "6mo") -> pd.DataFrame:
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df
