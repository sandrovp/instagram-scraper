from pathlib import Path
from loguru import logger as log
import asyncio
import json
from fastapi import FastAPI
import src.instagram as instagram
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Instagram Scraper API is running"}

@app.get("/scrape_user/{username}")
async def scrape_user(username: str):
    user = await instagram.scrape_user(username)
    return user

@app.get("/scrape_user_posts/{username}")
async def scrape_user_posts(username: str, max_pages: int = 3):
    posts_all = []
    async for post in instagram.scrape_user_posts(username, max_pages=max_pages):
        posts_all.append(post)
    log.success("scraped {} posts for user {}", len(posts_all), username)
    return posts_all