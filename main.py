import sys
import matplotlib.pyplot as plt
from utils import fetch_yahoo_headlines, analyze_sentiment, get_stock_change

def plot_sentiment_vs_return(sentiments, returns):
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    last_return = returns["Return"].iloc[-1] if not returns.empty else 0

    print(f"Average Sentiment: {avg_sentiment:.3f}")
    print(f"Last Day Return: {last_return:.3%}")

    plt.bar(["Sentiment", "Stock Return"], [avg_sentiment, last_return])
    plt.title("Sentiment vs. Stock Return")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    headlines = fetch_yahoo_headlines(ticker)
    sentiments = analyze_sentiment(headlines)
    returns = get_stock_change(ticker)
    plot_sentiment_vs_return(sentiments, returns)