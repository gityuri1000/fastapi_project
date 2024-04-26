from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import session_factory

class Session(ABC):
    ...

async def get_session() -> AsyncSession:
    async with session_factory() as session:
        yield session
        await session.commit()