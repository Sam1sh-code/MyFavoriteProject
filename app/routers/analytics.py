from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.services.analytics_scraping import generate_crypto_plot, get_cached_plot
import os

router = APIRouter()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

@router.get("/analytics", response_class=HTMLResponse)
async def analytics(request: Request, days: int = 7):
    # Разрешенные значения
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