from datetime import datetime, timedelta
from fastapi import HTTPException, Cookie
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# ---------------- Password hashing ----------------

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


# ---------------- JWT creation ----------------

def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ---------------- JWT validation ----------------

def get_current_user(access_token: str = Cookie(None)) -> str:
    """
    Проверяет JWT из cookie.
    Возвращает username если токен валиден.
    """

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        payload = jwt.decode(
            access_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token expired or invalid"
        )