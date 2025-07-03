# Stock News Sentiment Analyzer

A Streamlit app that fetches stock price history, recent news, applies sentiment analysis, technical indicators, and outputs actionable insights.

## Features

- Fetches historical price data with `yfinance`
- Retrieves news via NewsAPI
- Performs sentiment analysis with `vaderSentiment`
- Calculates technical indicators: RSI, SMA, MACD
- Placeholder ML model for trading signal suggestion

## Installation

```bash
pip install -r requirements.txt
export NEWS_API_KEY="your_key_here"
streamlit run app.py
