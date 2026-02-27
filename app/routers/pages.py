from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )


@router.get("/support")
def support():
    return {"message": "Support is not implemented yet 🙂"}