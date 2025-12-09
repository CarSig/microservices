# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# load_dotenv()
# from config import config

# engine = create_engine(config.POSTGRES.DATABASE_URL, future=True)

# print(f"Connecting to database at {config.POSTGRES.DATABASE_URL}")

# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

# # Dependency for FastAPI
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from config import config

DATABASE_URL = config.POSTGRES.DATABASE_URL.replace("psycopg2", "asyncpg")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
