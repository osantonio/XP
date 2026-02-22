from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from app.config import Config

engine = create_async_engine(Config.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker[AsyncSession](engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        # Import models here to ensure they are registered in SQLModel.metadata
        from app import models
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
