import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_yahoo_headlines(ticker="AAPL"):
    url = f"https://finance.yahoo.com/quote/{ticker}?p={ticker}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")
    headlines = []

    for li in soup.find_all("li"):
        if li.find("a"):
            text = li.text.strip()
            if text and len(text.split()) > 3:
                headlines.append(text)
    return headlines


def analyze_sentiment(headlines):
    sia = SentimentIntensityAnalyzer()
    scores = [sia.polarity_scores(headline)["compound"] for headline in headlines]
    return scores


def get_stock_change(ticker="AAPL"):
    data = yf.download(ticker, period="5d")
    data["Return"] = data["Close"].pct_change()
    return data[["Close", "Return"]]


def fetch_sentiment_timeseries(ticker="AAPL"):
    sia = SentimentIntensityAnalyzer()
    today = datetime.now().date()
    sentiment_by_date = {}

    for i in range(5):
        date = today - timedelta(days=i)
        url = f"https://finance.yahoo.com/quote/{ticker}/?p={ticker}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        headlines = []

        for li in soup.find_all("li"):
            if li.find("a"):
                text = li.text.strip()
                if text and len(text.split()) > 3:
                    headlines.append(text)

        if headlines:
            scores = [sia.polarity_scores(h)["compound"] for h in headlines]
            sentiment_by_date[date] = sum(scores) / len(scores)

    return pd.Series(sentiment_by_date).sort_index()