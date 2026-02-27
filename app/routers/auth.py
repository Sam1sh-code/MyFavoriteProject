from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.user_service import (
    register_user,
    authenticate_user,
)
from app.core.security import create_access_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES

from app.db.database import engine
from app.db.models import users
from sqlalchemy import select

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
@router.get("/register")
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):

    try:
        register_user(username, password)
    except Exception:
        raise HTTPException(status_code=400, detail="User already exists")

    return RedirectResponse(url="/login", status_code=302)


@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):

    user = authenticate_user(username, password)

    if not user:
        raise HTTPException(status_code=401, detail="Wrong username or password")

    access_token = create_access_token(user)

    response = RedirectResponse(url="/profile", status_code=302)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

    return response