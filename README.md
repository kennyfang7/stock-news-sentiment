# Stock News Sentiment Analysis

This project scrapes financial news headlines, performs sentiment analysis using VADER, and compares sentiment to recent stock price movements.

## Features
- Scrapes headlines from Yahoo Finance
- Analyzes sentiment with NLTK's VADER
- Fetches historical stock data with yfinance
- Visualizes sentiment vs stock return

## Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('vader_lexicon')"
```

## Usage
```bash
python main.py AAPL
```

---