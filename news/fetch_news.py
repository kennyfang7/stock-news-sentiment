from newsapi import NewsApiClient
from config import NEWS_API_KEY
from .sentiment_analysis import get_sentiment_score
from datetime import datetime, timedelta
import pandas as pd

def fetch_and_score(ticker: str, n_articles: int = 10):
    api = NewsApiClient(api_key=NEWS_API_KEY)
    query = f"{ticker} stock"
    
    # Try to cover ~3 days per article
    days_to_cover = n_articles * 3
    from_date = (datetime.now() - timedelta(days=days_to_cover)).strftime('%Y-%m-%d')
    to_date = datetime.now().strftime('%Y-%m-%d')
    
    res = api.get_everything(
        q=query,
        language="en",
        sort_by="publishedAt",
        from_param=from_date,
        to=to_date,
        page_size=100  # max allowed by NewsAPI
    )
    
    articles = res.get("articles", [])
    if not articles:
        return []

    # Convert to DataFrame for filtering by spaced-out dates
    df = pd.DataFrame(articles)
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df.sort_values(by='publishedAt', inplace=True)

    spaced_articles = []
    last_date = None

    for _, row in df.iterrows():
        pub_date = row['publishedAt']
        if last_date is None or (pub_date - last_date).days >= 3:
            spaced_articles.append({
                "title": row.get("title", ""),
                "url": row.get("url"),
                "publishedAt": pub_date.strftime('%Y-%m-%d'),
                "sentiment": get_sentiment_score(row.get("title", ""))
            })
            last_date = pub_date

        if len(spaced_articles) >= n_articles:
            break

    return spaced_articles
