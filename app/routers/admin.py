from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.services.user_service import get_user_from_db, get_all_users_from_db
import os

from app.db.models import users
from sqlalchemy import delete
from app.db.database import engine
from sqlalchemy import update
from fastapi.responses import RedirectResponse

router = APIRouter()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))

# @router.get("/adminus")
# def read_all_users(
#     request: Request,):
#     return templates.TemplateResponse(
#                 "admin_users.html")
    
    
@router.get("/admin")
def read_all_users(
    request: Request,
    current_user: str = Depends(get_current_user)):

    user_data = get_user_from_db(current_user)
    all_users = get_all_users_from_db()
    
    if not user_data:
        
        raise HTTPException(status_code=401, detail="Wrong status")
    
    if user_data.get('role') == "admin":
        

        return templates.TemplateResponse(
            "admin_users.html",
            {"request": request, "users": all_users}
        )     
    
    else:
        raise HTTPException(status_code=403, detail="You're not admin!")

@router.post("/admin/delete-user/{username}")
def delete_user(
    username: str,
    current_user: dict = Depends(get_current_user)
):
    user_data = get_user_from_db(current_user)

    if username == current_user:
        raise HTTPException(status_code=400, detail="You cannot delete yourself")


    if user_data.get('role') == "admin":
        with engine.connect() as conn:

            query = delete(users).where(users.c.username == username)
            result = conn.execute(query)
            conn.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": f"User {username} deleted"}
    
    else:
        raise HTTPException(status_code=403, detail="You're not admin!")



@router.post("/admin/change-role")
def change_role(
    username: str = Form(...),
    new_role: str = Form(...),
    current_user: dict = Depends(get_current_user) # Твоя проверка токена
):
    user_data = get_user_from_db(current_user)
    
    if user_data.get('role') == "admin":

        allowed_roles = ["admin", "user", "guest"]
        if new_role not in allowed_roles:
            raise HTTPException(status_code=400, detail="Invalid role")

        
        with engine.connect() as conn:
            query = update(users).where(
                users.c.username == username
            ).values(role=new_role)

            result = conn.execute(query)
            conn.commit()

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="User not found")

        # 3. ВАЖНО: Возвращаем админа на страницу со списком
        return RedirectResponse(url="/admin", status_code=303)
    
    else:
        raise HTTPException(status_code=403, detail="You're not admin!")
    
