from sqlalchemy import select, insert
from app.db.database import engine
from app.db.models import users
from app.core.security import hash_password, verify_password


def register_user(username: str, password: str):

    conn = engine.connect()

    query = select(users).where(users.c.username == username)
    existing_user = conn.execute(query).fetchone()

    if existing_user:
        conn.close()
        raise Exception("User already exists")

    hashed = hash_password(password)

    insert_query = insert(users).values(
        username=username,
        hashed_password=hashed
    )

    conn.execute(insert_query)
    conn.commit()
    conn.close()


def authenticate_user(username: str, password: str):

    conn = engine.connect()
    query = select(users).where(users.c.username == username)
    result = conn.execute(query).fetchone()
    conn.close()

    if not result:
        return False

    if not verify_password(password, result.hashed_password):
        return False

    return result.username

def get_user_from_db(username: str):
    conn = engine.connect()

    query = select(users).where(users.c.username == username)
    result = conn.execute(query).fetchone()

    conn.close()

    if result:
        return {
            "id": result.id,
            "username": result.username,
            "hashed_password": result.hashed_password
        }

    return None
