from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post_schema import PostCreate

def create_post(db: Session, post: PostCreate):
    existing_post = db.query(Post).filter(Post.reddit_id == post.reddit_id).first()
    if existing_post:
        print(f"Post with reddit_id {post.reddit_id} already exists. Skipping.")
        return existing_post

    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts_by_ticker(db: Session, ticker: str):
    return db.query(Post).filter(Post.ticker == ticker).all()


def get_trending_tickers(db: Session):
    from sqlalchemy import func
    return db.query(Post.ticker, func.count(Post.ticker).label("count")).group_by(Post.ticker).order_by(func.count(Post.ticker).desc()).limit(10).all()

