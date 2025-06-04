# app/etl/load.py
from app.db.session import SessionLocal
from app.crud.post_crud import create_post
from app.schemas.post_schema import PostCreate

def save_posts(posts: list[PostCreate]):
    db = SessionLocal()
    for post in posts:
        create_post(db, post)
    db.close()
