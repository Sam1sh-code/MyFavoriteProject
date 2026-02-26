from fastapi import FastAPI, Depends, HTTPException, Request, Form, Cookie
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os
from fastapi.staticfiles import StaticFiles
from fastapi import Response 


# Этот код найдет папку templates, где бы ни был запущен скрипт
base_dir = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))
app= FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

security = HTTPBearer()



SECRET_KEY = "supersecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

users_db = {
  "max": {
      "username": "max",
      "hashed_password": "..."
  }
}

def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "exp": expire
    }

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.get('/register')
def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    
    if username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    pw_num = ('0123456789')

    if len(password) >= 8 and any(char.isdigit() for char in pw_num):           #Пистая проверка на надежность пароля 


        hashed = hash_password(password)

        users_db[username] = {
            "username": username,
            "hashed_password": hashed
        }

        return RedirectResponse(url="/login")   
    
    elif len(password) < 8 or any(char.isfigit() for char in pw_num): 
        return {"messege" : "Password must have num and more then 8 len"}


@app.get('/')
def index_nothing(request: Request):
    return templates.TemplateResponse('index.html', {'request' : request})

@app.get('/login')
def login_get(request: Request):
    return templates.TemplateResponse('login.html', {"request":request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(username)

    # Создаём redirect
    response = RedirectResponse(url="/profile", status_code=302)

    # Ставим cookie на этот redirect
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60
    )

    return response

@app.get('/support')
def support(request: Request):
    return {"messege": {"Хах какая нaхуй поддержка? Ты в это поверил???"}}

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})

security = HTTPBearer()

def get_current_user(access_token: str = Cookie(None)):
    """
    Проверяет JWT-токен, который хранится в cookie 'access_token'.
    Возвращает имя пользователя, если токен валидный.
    """
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")

from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/profile")
def profile(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse(
        "profile.html",
        {"request": request, "username": current_user}
    )

