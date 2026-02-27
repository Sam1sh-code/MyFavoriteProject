from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

@router.get('/analytics')
def page_analitics(request: Request):

    return templates.TemplateResponse(
        "analytics.html",
        {"request": request}
    )
