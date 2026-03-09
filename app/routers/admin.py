# from fastapi import APIRouter, Request, Depends
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# from app.services.user_service import get_db, get_all_users
# from sqlalchemy.orm import Session
# import os

# router = APIRouter()

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))


# @router.get("/admin/users")
# def read_all_users(db: Session = Depends(get_db)):
#     return get_all_users(db)
