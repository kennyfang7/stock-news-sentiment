import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import NEWS_API_KEY
from data.historical_data import fetch_stock_history
from news.fetch_news import fetch_and_score
from prediction.features import add_technical_indicators
from prediction.model import predict_signal
from utils.helpers import format_sentiment, aggregate_sentiment

st.set_page_config(page_title="Stock News & Sentiment Analyzer", layout="wide")
st.title("📈 Stock News & Sentiment Analyzer")

# --- User Inputs ---
ticker = st.text_input("Enter stock ticker (e.g. AAPL)", value="AAPL").upper()
n_articles = st.slider("Number of news articles", min_value=1, max_value=50, value=10)
space_out_articles = st.checkbox("Space out news articles by 3 days", value=True)  # ✅ NEW

if st.button("Analyze") and ticker:
    # --- Price History ---
    hist = fetch_stock_history(ticker)
    st.subheader(f"📊 Price History for {ticker}")

    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(
        x=hist.index, y=hist["Close"],
        name="Close Price", line=dict(color='royalblue')
    ))

    fig_price.update_layout(
        xaxis=dict(
            title="Date",
            range=[hist.index.min(), hist.index.max()],
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis_title="Price (USD)",
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    st.plotly_chart(fig_price, use_container_width=True)

    # --- Technical Indicators ---
    features = add_technical_indicators(hist)
    st.subheader("📈 Technical Indicators")

    fig_ind = make_subplots(specs=[[{"secondary_y": True}]])
    fig_ind.add_trace(go.Scatter(x=features.index, y=features["RSI"], name="RSI", line=dict(color='orange')), secondary_y=False)
    fig_ind.add_trace(go.Scatter(x=features.index, y=features["SMA_20"], name="SMA 20", line=dict(color='green')), secondary_y=True)
    fig_ind.add_trace(go.Scatter(x=features.index, y=features["MACD"], name="MACD", line=dict(color='purple')), secondary_y=True)

    fig_ind.update_layout(
        xaxis=dict(
            title="Date",
            range=[features.index.min(), features.index.max()],
            rangeslider=dict(visible=True),
            type="date"
        ),
        yaxis=dict(title="RSI", range=[0, 100]),
        yaxis2=dict(title="SMA / MACD", overlaying='y', side='right'),
        height=450,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_ind, use_container_width=True)

    # --- News & Sentiment ---
    st.subheader("🗞️ News & Sentiment")

    news = fetch_and_score(ticker, n_articles, space_out_articles)  # ✅ UPDATED
    if news:
        df_news = pd.DataFrame(news)
        df_news["formatted"] = df_news["sentiment"].apply(format_sentiment)
        st.dataframe(df_news[["publishedAt", "title", "formatted", "sentiment"]], use_container_width=True)

        avg_sent = aggregate_sentiment(df_news["sentiment"].tolist())
        st.markdown(f"**🧠 Average Sentiment Score:** `{avg_sent:.2f}`")

        # 📈 Sentiment Over Time
        sentiment_by_day = df_news.groupby("publishedAt")["sentiment"].mean().reset_index()

        fig_sent = go.Figure()
        fig_sent.add_trace(go.Scatter(
            x=sentiment_by_day["publishedAt"],
            y=sentiment_by_day["sentiment"],
            mode="lines+markers",
            name="Average Sentiment",
            line=dict(color="crimson")
        ))

        fig_sent.update_layout(
            title="🧠 Sentiment Over Time",
            xaxis_title="Date",
            yaxis_title="Average Sentiment",
            yaxis=dict(range=[-1, 1]),
            height=400,
            margin=dict(l=40, r=40, t=40, b=40),
        )

        st.plotly_chart(fig_sent, use_container_width=True)

    else:
        st.warning("No news articles found. Try increasing the time range or reducing filters.")

    # --- Placeholder Prediction Signal ---
    signal = predict_signal(features)
    st.markdown(f"### 📊 Suggested action: **{signal.upper()}**")

    # --- Notes ---
    st.write("---")
    st.markdown("💡 _Future upgrades may include:_")
    st.markdown("- FinBERT for more accurate financial sentiment")
    st.markdown("- Strategy backtesting")
    st.markdown("- Portfolio tracker for multiple tickers")
