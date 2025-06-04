# app/etl/extract.py
import praw

def get_reddit_client():
    return praw.Reddit(
        client_id="SvOOHrEJjtSzKYpBuOE9Yg",
        client_secret="qQmXzHPYj5eyF0xlV4_wTqkr8yOZHg",
        user_agent="sentiment_scraper:v1.0 (by u/Brilliant-Coach-9632)"
    )

def fetch_reddit_posts(limit=1000):
    reddit = get_reddit_client()
    subreddit = reddit.subreddit("wallstreetbets")
    return subreddit.new(limit=limit)
