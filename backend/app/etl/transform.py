# app/etl/transform.py
import re
from datetime import datetime
from app.schemas.post_schema import PostCreate

ALLOWED_FLAIRS = {
    "DD", "Discussion", "News", "YOLO", "Gain", "Loss",
    "Earnings Thread", "Daily Discussion"
}
TARGET_TICKERS = {"TSLA", "AAPL"}
TARGET_KEYWORDS = {"tesla", "apple"}

def clean_text(text: str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^A-Za-z0-9\s\$]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_tickers(text: str) -> list[str]:
    matches = re.findall(r"\$?[A-Z]{2,5}", text)
    return [m.replace("$", "") for m in matches if m.isupper() and not m.isdigit()]

def transform_submission(submission) -> PostCreate | None:
    if submission.score < 10:
        return None

    flair = submission.link_flair_text or ""
    if flair not in ALLOWED_FLAIRS:
        return None

    title = clean_text(submission.title)
    body = clean_text(submission.selftext)
    combined_text = f"{title} {body}"
    combined_lower = combined_text.lower()

    tickers = extract_tickers(combined_text)
    tickers_set = set(tickers)

    if not (tickers_set & TARGET_TICKERS or any(kw in combined_lower for kw in TARGET_KEYWORDS)):
        return None

    # Determine ticker
    ticker = next((t for t in tickers if t in TARGET_TICKERS), None)
    if not ticker:
        if "tesla" in combined_lower:
            ticker = "TSLA"
        elif "apple" in combined_lower:
            ticker = "AAPL"

    if not ticker:
        return None

    return PostCreate(
        reddit_id=submission.id,
        ticker=ticker,
        title=title,
        body=body,
        sentiment="neutral",
        confidence=0.0,
        created_at=datetime.utcfromtimestamp(submission.created_utc),
        score=submission.score,
        author=submission.author.name if submission.author else "unknown"
    )
