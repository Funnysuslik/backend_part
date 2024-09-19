from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# Load environment variables
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")
# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory (used to interact with the database)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession  # Ensures we're using async sessions
)

# Dependency to get DB session for request
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
