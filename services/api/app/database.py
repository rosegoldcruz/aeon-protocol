import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Neon PostgreSQL Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgres://neondb_owner:npg_uD6OmlzEb0Lh@ep-aged-snow-ad22bt8l-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
)

# Convert postgres:// to postgresql+asyncpg:// for SQLAlchemy async
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Async engine and session
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
