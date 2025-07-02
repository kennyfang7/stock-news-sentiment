import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from utils import (
    fetch_yahoo_headlines,
    analyze_sentiment,
    fetch_sentiment_timeseries
)

st.set_page_config(page_title="Stock Sentiment Dashboard", layout="wide")

st.title("📈 Stock Sentiment Analysis Dashboard")
st.markdown("""
Enter a stock ticker below to view recent news sentiment trends alongside stock performance.
""")

# Sidebar for ticker input
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", value="AAPL")
days = st.sidebar.slider("Sentiment Time Window (Days)", min_value=7, max_value=90, value=30, step=3)

if ticker:
    with st.spinner("Fetching data and analyzing sentiment..."):
        headlines = fetch_yahoo_headlines(ticker)
        sentiments = analyze_sentiment(headlines)
        stock_data = yf.download(ticker, period=f"{days}d")
        sentiment_series = fetch_sentiment_timeseries(ticker, days=days)

    # Layout: Charts on top, headlines below
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Sentiment vs. Stock Return")
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0

        if not stock_data.empty:
            last_close = stock_data["Close"].iloc[-1]
            first_close = stock_data["Close"].iloc[0]

            if hasattr(last_close, 'item'):
                last_close = last_close.item()
            if hasattr(first_close, 'item'):
                first_close = first_close.item()

            pct_change = ((last_close - first_close) / first_close) if first_close != 0 else 0
        else:
            pct_change = 0

        fig, ax = plt.subplots()
        ax.bar(["Avg Sentiment", "% Stock Change"], [avg_sentiment, pct_change])
        ax.set_title("Average Sentiment vs. Stock Change")
        ax.grid(True)
        st.pyplot(fig)

    with col2:
        st.subheader("📉 Sentiment Time Series with Stock Price")
        if not sentiment_series.empty and not stock_data.empty:
            fig, ax1 = plt.subplots(figsize=(10, 5))
            ax1.set_title(f"{ticker} Sentiment & Stock Price Over {days} Days")
            sentiment_series.plot(ax=ax1, color='tab:blue', marker='o', label="Sentiment")
            ax1.set_ylabel("Sentiment", color='tab:blue')
            ax1.tick_params(axis='y', labelcolor='tab:blue')
            
            ax2 = ax1.twinx()
            stock_data["Close"].plot(ax=ax2, color='tab:green', label="Close Price")
            ax2.set_ylabel("Stock Price", color='tab:green')
            ax2.tick_params(axis='y', labelcolor='tab:green')

            ax1.grid(True)
            fig.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Not enough data to plot sentiment or price.")

    st.subheader("📰 Latest Headlines")
    if headlines:
        for h in headlines[:10]:
            st.markdown(f"- {h}")
    else:
        st.write("No headlines found.")