import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

# 🔑 PLACE YOUR NEWSAPI KEY HERE
NEWSAPI_KEY = "9d301a9505b042569d35387bddef276e"


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


def fetch_sentiment_timeseries(ticker="AAPL", days=365):
    sia = SentimentIntensityAnalyzer()
    today = datetime.utcnow().date()
    sentiment_by_date = {}

    for i in range(days):
        date = today - timedelta(days=i)
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": ticker,
            "from": date.isoformat(),
            "to": date.isoformat(),
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 100,
            "apiKey": NEWSAPI_KEY
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch news for {date}: {response.status_code}")
            continue

        articles = response.json().get("articles", [])
        headlines = [a["title"] for a in articles if a.get("title")]

        if headlines:
            scores = [sia.polarity_scores(h)["compound"] for h in headlines]
            sentiment_by_date[date] = sum(scores) / len(scores)

        time.sleep(1.2)  # Prevent hitting rate limits

    return pd.Series(sentiment_by_date).sort_index()
