from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db:5432/fastapi_db")

# Engine async thực sự cho app
engine = create_async_engine(DATABASE_URL, echo=True)

# Session async
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
