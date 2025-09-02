import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get DATABASE_URL from env, fallback localhost for dev
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/blog_db"
)

# Async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Session maker
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

# Base model
Base = declarative_base()

# Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
