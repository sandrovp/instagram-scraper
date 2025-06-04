from pathlib import Path
from loguru import logger as log
from fastapi import FastAPI
import src.instagram as instagram
from fastapi.responses import JSONResponse
from fastapi import HTTPException




app = FastAPI()

@app.get("/scrape_user/{username}")
async def scrape_user(username: str):
    try:
        user = await instagram.scrape_user(username)
        return user
    except Exception as e:
        log.error(f"Erro ao buscar user {username}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/scrape_user_posts/{username}")
async def scrape_user_posts(username: str, max_pages: int = 3):
    try:
        posts_all = []
        async for post in instagram.scrape_user_posts(username, max_pages=max_pages):
            posts_all.append(post)
        log.success("scraped {} posts for user {}", len(posts_all), username)
        return JSONResponse(content=posts_all)
    except Exception as e:
        log.error(f"Erro ao buscar posts do user {username}: {e}")
        raise HTTPException(status_code=500, detail=str(e))