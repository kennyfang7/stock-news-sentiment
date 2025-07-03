import pandas as pd
import ta

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    df["SMA_20"] = ta.trend.SMAIndicator(df["Close"], window=20).sma_indicator()
    df["MACD"] = ta.trend.MACD(df["Close"]).macd()
    return df.dropna()
