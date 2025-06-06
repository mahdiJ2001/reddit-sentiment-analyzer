# backend/app/etl/deploy.py

from app.etl.pipeline import reddit_etl_flow

if __name__ == "__main__":
    reddit_etl_flow.serve(
        name="reddit-sentiment-daily-8am-utc",
        cron="0 8 * * *",  
        tags=["reddit", "sentiment", "etl", "production"],
        description="Daily Reddit WSB sentiment analysis pipeline - runs at 8 AM UTC"
    )
