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
    # Remove URLs
    text = re.sub(r"http\S+", "", text)  
    # Keep tickers, so commenting this out: text = re.sub(r"\$[A-Za-z]{1,5}", "", text)  
    # Remove non-alphanumeric except spaces and $
    text = re.sub(r"[^A-Za-z0-9\s\$]+", " ", text)
    text = re.sub(r"\s+", " ", text)  # normalize whitespace
    return text.strip()

def scrape_and_save(limit=10):
    db = SessionLocal()
    subreddit = reddit.subreddit("wallstreetbets")

    print(f"Starting scrape of subreddit 'wallstreetbets' with limit={limit}")

    count_saved = 0
    for submission in subreddit.hot(limit=limit):
        print(f"Checking post: {submission.title} (score: {submission.score})")

        if submission.score < 100:
            print("Skipping due to low score")
            continue  # filter posts by score > 100
        
        flair = submission.link_flair_text
        if flair not in ["DD", "Discussion", "News"]:
            print(f"Skipping due to flair: {flair}")
            continue
        
        title = clean_text(submission.title)
        body = clean_text(submission.selftext)

        tickers = re.findall(r"\$[A-Za-z]{1,5}", submission.title + " " + submission.selftext)
        if not tickers:
            print("Skipping post with no ticker found.")
            continue
        
        ticker = tickers[0].replace("$", "")
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


        print(f"Saving post: ticker={ticker}, title={title[:30]}..., author={post_data.author}")
        create_post(db, post_data)
        count_saved += 1

    db.close()
    print(f"Scraping done. Saved {count_saved} posts.")

if __name__ == "__main__":
    scrape_and_save()
