from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.engine_validation import settings

URI = str(settings.DATABASE_URI).replace("postgresql", "postgresql+asyncpg")
async_engine = create_async_engine(url=URI, echo=False)

session_factory = async_sessionmaker(bind=async_engine, autoflush=False, autocommit=False)