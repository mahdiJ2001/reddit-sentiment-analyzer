from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    reddit_id: str
    ticker: str
    title: str
    body: str
    sentiment: str
    confidence: float
    created_at: datetime
    score: int
    author: str

class PostCreate(PostBase):
    pass

class PostOut(PostBase):
    id: int

    class Config:
        orm_mode = True

