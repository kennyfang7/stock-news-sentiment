from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def get_sentiment_score(text: str) -> float:
    scores = analyzer.polarity_scores(text)
    return scores["compound"]
