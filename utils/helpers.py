import datetime

def format_sentiment(score: float) -> str:
    if score > 0.2:
        return "🟢 Positive"
    elif score < -0.2:
        return "🔴 Negative"
    return "🟡 Neutral"

def aggregate_sentiment(scores: list[float]) -> float:
    return sum(scores) / max(len(scores), 1)
