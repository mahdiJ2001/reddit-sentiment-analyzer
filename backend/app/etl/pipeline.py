# app/etl/pipeline.py

from app.etl.extract import fetch_reddit_posts
from app.etl.transform import transform_submission
from app.etl.load import save_posts

def run_pipeline():
    print("🔍 Extracting Reddit posts...")
    submissions = fetch_reddit_posts(limit=500)

    print("🔄 Transforming posts...")
    transformed_posts = []
    for submission in submissions:
        post = transform_submission(submission)
        if post:
            transformed_posts.append(post)

    print(f"✅ {len(transformed_posts)} posts ready to load.")

    print("💾 Saving posts to database...")
    save_posts(transformed_posts)

    print("🏁 ETL pipeline finished.")

# Run if called directly
if __name__ == "__main__":
    run_pipeline()
