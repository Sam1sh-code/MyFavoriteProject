from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.services.analytics_scraping import fetch_coin_data, get_cached_plot
import os
import time

router = APIRouter()
CACHE = {}
CACHE_TTL = 300  # 5 минут
COINS = ["bitcoin", "ethereum"]

# Путь к шаблонам
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# ------------------ HTML ------------------
@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request, days: int = 7):
    if days not in [7, 30, 90]:
        days = 7

    btc_file = get_cached_plot("bitcoin", days)
    eth_file = get_cached_plot("ethereum", days)

    return templates.TemplateResponse(
        "analytics.html",
        {
            "request": request,
            "btc_file": btc_file,
            "eth_file": eth_file,
            "days": days
        }
    )

# ------------------ API для JS ------------------
@router.get("/api/crypto")
async def get_crypto_data(coin: str = "bitcoin", days: int = 7):
    if days not in [7, 30, 90]:
        days = 7

    key = (coin, days)
    now = time.time()

    # Кэширование
    if key in CACHE and now - CACHE[key]["time"] < CACHE_TTL:
        return CACHE[key]["data"]

    data = fetch_coin_data(coin, days)
    result = {"coin": coin, "days": days, "data": data}

    CACHE[key] = {"time": now, "data": result}
    return result

# ------------------ Объединенный роут для всех монет ------------------
@router.get("/api/market")
async def get_market_data(days: int = 7):
    if days not in [7, 30, 90]:
        days = 7

    now = time.time()
    if days in CACHE and now - CACHE[days]["time"] < CACHE_TTL:
        return CACHE[days]["data"]

    result = {}
    for coin in COINS:
        result[coin] = fetch_coin_data(coin, days)

    payload = {"days": days, "data": result}
    CACHE[days] = {"time": now, "data": payload}
    return payload
