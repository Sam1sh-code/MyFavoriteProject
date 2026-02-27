from fastapi import FastAPI
from app.routers import auth, pages, profile
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(profile.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
















# from fastapi import FastAPI, Depends, HTTPException, Request, Form, Cookie
# from fastapi.security import HTTPBearer
# from jose import jwt, JWTError
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from datetime import datetime, timedelta
# from passlib.context import CryptContext
# import os
# from fastapi.staticfiles import StaticFiles
# from fastapi import Response 
# from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
# from sqlalchemy import insert, select


# # Этот код найдет папку templates, где бы ни был запущен скрипт
# base_dir = os.path.dirname(os.path.abspath(__file__))
# templates = Jinja2Templates(directory=os.path.join(base_dir, "templates"))
# app= FastAPI()


# DATABASE_URL = "sqlite:///./users.db"
# metadata = MetaData()
# engine = create_engine(DATABASE_URL)

# users = Table(
#     "users",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("username", String, unique=True, index=True),
#     Column("hashed_password", String),
# )

# metadata.create_all(engine)  # создаёт файл users.db и таблицу

# app.mount("/static", StaticFiles(directory="static"), name="static")

# security = HTTPBearer()



# SECRET_KEY = "supersecretkey123"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 5
# ##################Password#####################
# pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# def hash_password(password):
#     return pwd_context.hash(password)

# def verify_password(password, hashed):
#     return pwd_context.verify(password, hashed)
# ##############################################################
# # Регистрация/логин в bd sqlite
# def register_user(username: str, password: str):
#     hashed = hash_password(password)
#     query = insert(users).values(username=username, hashed_password=hashed)
#     conn = engine.connect()
#     try:
#         conn.execute(query)
#         conn.commit()
#     except Exception:
#         raise Exception("User already exists")
#     finally:
#         conn.close()

# def authenticate_user(username: str, password: str):
#     conn = engine.connect()
#     query = select(users).where(users.c.username == username)
#     result = conn.execute(query).fetchone()
#     conn.close()
#     if not result:
#         return False
#     if not verify_password(password, result.hashed_password):
#         return False
#     return result.username

# #############################JWT############################
# def create_access_token(username: str):
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     payload = {"sub": username, "exp": expire}
#     return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# #####################################################################

# def get_current_user(access_token: str = Cookie(None)):
#     """
#     Проверяет JWT-токен, который хранится в cookie 'access_token'.
#     Возвращает имя пользователя, если токен валидный.
#     """
#     if not access_token:
#         raise HTTPException(status_code=401, detail="Not authenticated")

#     try:
#         payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")

#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token")

#         return username

#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token expired or invalid")
# #####################################################get_user_from_db
# def get_user_from_db(username: str):
#     conn = engine.connect()

#     query = select(users).where(users.c.username == username)
#     result = conn.execute(query).fetchone()

#     conn.close()

#     if result:
#         return {
#             "id": result.id,
#             "username": result.username,
#             "hashed_password": result.hashed_password
#         }

#     return None

# #######################################################

# @app.get('/register')
# def get_register(request: Request):
#     return templates.TemplateResponse("register.html", {"request": request})

# @app.post("/register")
# def register(username: str = Form(...), password: str = Form(...)):
    
#     conn = engine.connect()
    
#     query = select(users).where(users.c.username == username)
#     existing_user = conn.execute(query).fetchone()

#     if existing_user:
#         conn.close()
#         raise HTTPException(status_code=400, detail="User already exists")
    
#     pw_num = ('0123456789')

#     if len(password) < 8 or not any(char.isdigit() for char in pw_num): 
#         conn.close()
#         return {"messege" : "Password must have num and more then 8 len"}
    
#     hashed = hash_password(password)

#     insert_query = users.insert().values(
#         username=username,
#         hashed_password=hashed
#     )

#     conn.execute(insert_query)
#     conn.commit()
#     conn.close()

    # return RedirectResponse(url="/login", status_code=302)


# @app.get('/')
# def index_nothing(request: Request):
#     return templates.TemplateResponse('index.html', {'request' : request})

# @app.get('/login')
# def login_get(request: Request):
#     return templates.TemplateResponse('login.html', {"request":request})

# @app.post("/login")
# def login(username: str = Form(...), password: str = Form(...)): 

#     user = authenticate_user(username, password)

#     if not user:
#         raise HTTPException(status_code=401, detail="Probobly your password or username wrong")
    
#     access_token = create_access_token(user)
#                         # Создаём redirect
#     response = RedirectResponse(url="/profile", status_code=302)

#             # Ставим cookie на этот redirect
#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         samesite="lax",
#         max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60
#     )
#     return response

# @app.get('/support')
# def support(request: Request):
#     return {"messege": {"Хах какая нaхуй поддержка? Ты в это поверил???"}}

# @app.get("/about")
# def about(request: Request):
#     return templates.TemplateResponse('about.html', {'request': request})


# @app.get("/profile", response_class=HTMLResponse)
# def profile(request: Request, current_user: str = Depends(get_current_user)):
#     return templates.TemplateResponse(
#         "profile.html",
#         {
#             "request": request,
#             "username": current_user
#         }
#     )

# @app.get("/profile", response_class=HTMLResponse)
# def profile(request: Request, current_user: str = Depends(get_current_user)):
#     # Тут ты можешь достать данные пользователя из БД
#     # Пока сделаем пример

#     user_data = get_user_from_db(current_user)

#     if not user_data:
#         raise HTTPException(status_code=404, detail="User not found")

#     my_user_info = {
#         "username": "Admin_FastAPI",
#         "status": "Разрабатываю проект"
#     }
#     return templates.TemplateResponse("profile.html", {
#         "request": request, 
#         "user": my_user_info # Вот этот ключ 'user' мы используем в HTML
#     })
