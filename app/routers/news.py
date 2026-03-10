from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.services.analytics_scraping import fetch_coin_data, get_cached_plot
from app.core.security import get_current_user
from app.services.user_service import get_user_from_db
from app.services.news_scraping import get_bbc_news
import os
import time
router = APIRouter()
CACHE = {}
CACHE_TTL = 300  # 5 минут
COINS = ["bitcoin", "ethereum"]

# Путь к шаблонам
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

@router.get("/news", response_class=HTMLResponse)
def get_news_last_7d(
    request: Request,
    current_user: str = Depends(get_current_user)
):
    user_data = get_user_from_db(current_user)

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    news_data = get_bbc_news()

    return templates.TemplateResponse("news.html", {"request": request, "news": news_data})

# @router.get("/news")
# async def read_news(request: Request):
    
#     return templates.TemplateResponse("news.html", {"request": request, "news": news_data})