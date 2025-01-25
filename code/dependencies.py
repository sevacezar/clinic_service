"""Module with global dependencies"""

from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session


async def get_session() -> AsyncSession:
    """Function of async sessions getting."""
    async with async_session() as session:
        yield session