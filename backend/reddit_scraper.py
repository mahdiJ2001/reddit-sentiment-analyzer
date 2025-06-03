import praw
import re
from app.crud.post_crud import create_post
from app.db.session import SessionLocal
from app.schemas.post_schema import PostCreate
from datetime import datetime

# Initialize PRAW client
reddit = praw.Reddit(
    client_id="SvOOHrEJjtSzKYpBuOE9Yg",
    client_secret="qQmXzHPYj5eyF0xlV4_wTqkr8yOZHg",
    user_agent="sentiment_scraper:v1.0 (by u/Brilliant-Coach-9632)"
)

def clean_text(text: str) -> str:
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^A-Za-z0-9\s\$]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_tickers(text: str) -> list[str]:
    matches = re.findall(r"\$?[A-Z]{2,5}", text)
    return [m.replace("$", "") for m in matches if m.isupper() and not m.isdigit()]

def scrape_and_save(limit=1000):
    db = SessionLocal()
    subreddit = reddit.subreddit("wallstreetbets")

    print(f"Starting scrape of subreddit 'wallstreetbets' with limit={limit}")

    allowed_flairs = [
        "DD", "Discussion", "News", "YOLO", "Gain", "Loss",
        "Earnings Thread", "Daily Discussion"
    ]

    target_tickers = {"TSLA", "AAPL"}
    target_keywords = {"tesla", "apple"}  

    count_saved = 0

    for submission in subreddit.new(limit=limit):
        print(f"Checking post: {submission.title} (score: {submission.score})")

        if submission.score < 10:
            continue

        flair = submission.link_flair_text or ""
        if flair not in allowed_flairs:
            continue

        title = clean_text(submission.title)
        body = clean_text(submission.selftext)
        combined_text = title + " " + body
        combined_lower = combined_text.lower()

        tickers = extract_tickers(combined_text)
        tickers_set = set(tickers)

        mentions_target_ticker = tickers_set & target_tickers
        mentions_target_keyword = any(kw in combined_lower for kw in target_keywords)

        if not (mentions_target_ticker or mentions_target_keyword):
            continue  # Skip if no relevant ticker or company name mentioned

        # Decide which ticker to assign (priority to symbol if both present)
        ticker = None
        for t in tickers:
            if t in target_tickers:
                ticker = t
                break
        if not ticker:
            if "tesla" in combined_lower:
                ticker = "TSLA"
            elif "apple" in combined_lower:
                ticker = "AAPL"

        # If ticker still None, skip this post to satisfy type requirements
        if ticker is None:
            print(f"Skipping post {submission.id} due to no assignable ticker.")
            continue

        created_at = datetime.utcfromtimestamp(submission.created_utc)

        post_data = PostCreate(
            reddit_id=submission.id,
            ticker=ticker,
            title=title,
            body=body,
            sentiment="neutral",
            confidence=0.0,
            created_at=created_at,
            score=submission.score,
            author=submission.author.name if submission.author else "unknown"
        )

        print(f"Saving post: {ticker} - {title[:40]}... by {post_data.author}")
        create_post(db, post_data)
        count_saved += 1

    db.close()
    print(f"Scraping complete. {count_saved} relevant posts saved.")

if __name__ == "__main__":
    scrape_and_save()
