# database.py (Sync version)
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from redis import Redis
from dotenv import load_dotenv
from .models.base import Base  # chỉ import metadata

load_dotenv()

# URLs
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/fastapi_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# PostgreSQL sync engine (create_engine with psycopg2)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Redis client
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    try:
        yield redis_client
    finally:
        redis_client.close()
