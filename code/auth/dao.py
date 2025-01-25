"""Module with data access object of auth"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import User

class UsersDAO:
    async def get_user_by_username(
            session: AsyncSession,
            username: str,
        ) -> User | None:
        """Get user by username"""
        query = select(User).where(User.username == username).options(selectinload(User.role))
        res = await session.execute(query)
        return res.scalar_one_or_none()
