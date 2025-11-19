# backend/app/db.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models.user import Base # Import Base from your models

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        # This will create the tables
        await conn.run_sync(Base.metadata.create_all)