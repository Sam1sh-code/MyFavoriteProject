from fastapi import FastAPI, Request
from app.routers import auth, pages, profile, analytics
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from app.db.database import engine, metadata
from app.db import models

metadata.create_all(engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(profile.router)
app.include_router(analytics.router)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "app/templates"))

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(404)
async def custom_404_handler(request: Request, __):
    return templates.TemplateResponse("404.html", {
        "request": request
    }, status_code=404)

@app.exception_handler(401)
async def custom_404_handler(request: Request, __):
    return templates.TemplateResponse("401.html", {
        "request": request
    }, status_code=401)
