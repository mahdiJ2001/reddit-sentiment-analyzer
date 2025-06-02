from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.post_schema import PostCreate, PostOut
from app.crud.post_crud import create_post, get_posts_by_ticker, get_trending_tickers
from app.db.session import get_db

router = APIRouter()

@router.post("/", response_model=PostOut)
def create(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db, post)

@router.get("/ticker/{ticker}", response_model=list[PostOut])
def read_posts_by_ticker(ticker: str, db: Session = Depends(get_db)):
    return get_posts_by_ticker(db, ticker)

@router.get("/trending")
def trending(db: Session = Depends(get_db)):
    return get_trending_tickers(db)