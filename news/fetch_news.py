from newsapi import NewsApiClient
from config import NEWS_API_KEY
from .sentiment_analysis import get_sentiment_score
from datetime import datetime, timedelta
import pandas as pd

def fetch_and_score(ticker: str, n_articles: int = 10, space_out: bool = True, min_spacing_days: int = 2):
    api = NewsApiClient(api_key=NEWS_API_KEY)
    query = f"{ticker} stock"

    # Limit to max 30 days due to free NewsAPI tier
    days_to_cover = min(n_articles * 6, 30)
    from_date = (datetime.now() - timedelta(days=days_to_cover)).strftime('%Y-%m-%d')
    to_date = datetime.now().strftime('%Y-%m-%d')

    res = api.get_everything(
        q=query,
        language="en",
        sort_by="publishedAt",
        from_param=from_date,
        to=to_date,
        page_size=100
    )

    articles = res.get("articles", [])
    if not articles:
        return []

    df = pd.DataFrame(articles)
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df.sort_values(by='publishedAt', inplace=True)

    spaced_articles = []
    last_date = None
    min_spacing = timedelta(days=min_spacing_days)

    for _, row in df.iterrows():
        pub_date = row['publishedAt']
        if not space_out or last_date is None or (pub_date - last_date) >= min_spacing:
            spaced_articles.append({
                "title": row.get("title", ""),
                "url": row.get("url"),
                "publishedAt": pub_date.strftime('%Y-%m-%d'),
                "sentiment": get_sentiment_score(row.get("title", ""))
            })
            last_date = pub_date

        if len(spaced_articles) >= n_articles:
            break

    # --- Fallback: If not enough spaced articles, return most recent articles ignoring spacing ---
    if len(spaced_articles) < n_articles:
        fallback_articles = []
        df_sorted = df.sort_values(by='publishedAt', ascending=False)
        for _, row in df_sorted.iterrows():
            fallback_articles.append({
                "title": row.get("title", ""),
                "url": row.get("url"),
                "publishedAt": row['publishedAt'].strftime('%Y-%m-%d'),
                "sentiment": get_sentiment_score(row.get("title", ""))
            })
            if len(fallback_articles) >= n_articles:
                break
        return fallback_articles

    return spaced_articles
