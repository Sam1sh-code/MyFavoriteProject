from sqlalchemy import create_engine, MetaData
from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()