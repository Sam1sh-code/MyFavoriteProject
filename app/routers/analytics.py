from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.services.analytics_scraping import generate_crypto_plot
import os

router = APIRouter()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

@router.get("/analytics", response_class=HTMLResponse)
def get_analytics(request: Request, days: int = 7):

    if days not in [7, 30, 90]:
        days = 7

    generate_crypto_plot("bitcoin", "btc_chart.png", days)
    generate_crypto_plot("ethereum", "eth_chart.png", days)

    return templates.TemplateResponse(
        "analytics.html",
        {"request": request}
    )