from fastapi import FastAPI
from app.routers import auth, pages, profile, analytics
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(profile.router)
app.include_router(analytics.router)

app.mount("/static", StaticFiles(directory="static"), name="static")