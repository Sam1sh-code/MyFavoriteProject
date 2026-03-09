from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
import os

from app.core.security import get_current_user
from app.services.user_service import get_user_from_db

router = APIRouter()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))


@router.get("/profile")
def profile(
    request: Request,
    current_user: str = Depends(get_current_user)
):
    user_data = get_user_from_db(current_user)

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    print(user_data)
    
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": user_data
        }
    )