from fastapi import FastAPI
from app.routers import post_routes

app = FastAPI()
app.include_router(post_routes.router, prefix="/posts", tags=["Posts"])