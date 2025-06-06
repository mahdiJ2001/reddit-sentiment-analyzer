# backend/app/etl/pipeline.py
from prefect import flow, task
from app.etl.extract import fetch_reddit_posts
from app.etl.transform import transform_submission
from app.etl.load import save_posts
from datetime import timedelta
from prefect.tasks import task_input_hash
from datetime import datetime

# Cache the extraction for 1 hour to avoid duplicate processing
@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def extract():
    print("🔍 Extracting Reddit posts...")
    return fetch_reddit_posts(limit=500)

@task
def transform(submissions):
    print("🔄 Transforming posts...")
    transformed_posts = []
    for submission in submissions:
        post = transform_submission(submission)
        if post:
            transformed_posts.append(post)
    print(f"✅ {len(transformed_posts)} posts ready to load.")
    return transformed_posts

@task
def load(transformed_posts):
    print("💾 Saving posts to database...")
    save_posts(transformed_posts)

@flow(name="Reddit Sentiment Pipeline", 
      description="ETL pipeline for WSB sentiment analysis",
      retries=3, 
      retry_delay_seconds=60)
def reddit_etl_flow():
    submissions = extract()
    transformed_data = transform(submissions)
    load(transformed_data)

if __name__ == "__main__":
    reddit_etl_flow()