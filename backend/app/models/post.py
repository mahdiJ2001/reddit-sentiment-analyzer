from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from app.db.base import Base
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    title = Column(Text)
    body = Column(Text)
    sentiment = Column(String)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer)
    author = Column(String)
