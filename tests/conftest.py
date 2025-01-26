"""Module with common tests functionality"""

import asyncio
import sys, os
from typing import Any

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../code')))

from auth.auth import get_password_hash
from auth.models import User, Role
from database import Base
from dependencies import get_session
from main import app

DATABASE_URL_TESTS = 'postgresql+asyncpg://postgres:postgres@localhost:5433/postgres'

engine = create_async_engine(url=DATABASE_URL_TESTS, poolclass=NullPool)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def override_get_session() -> AsyncSession:
    """Generate async test-DB-sessions"""
    async with async_session() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope='function', autouse=True)
async def setup_database():
    """Fixture of database setup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope='function')
async def db() -> AsyncSession:
    """Generate async DB-session."""
    async with async_session() as session:
        yield session

@pytest.fixture(scope='function')
async def client() -> AsyncClient:
    """Generate async client for requests"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac

@pytest.fixture(scope='function')
async def test_user_doctor(db: AsyncSession) -> dict[str, Any]:
    """Fixture of getting test user with doctor role"""
    username: str = 'best_doctor'
    password: str = 'some_dificult_password'
    hashed_password: str = get_password_hash(password=password)
    user = User(username=username, password_hashed=hashed_password)
    role = Role(name='doctor')
    user.role = role
    db.add(user)
    await db.commit()
    return {'username': username, 'password': password, 'user': user}

@pytest.fixture(scope='function')
async def test_user_not_doctor(db: AsyncSession) -> dict[str, Any]:
    """Fixture of getting test user without doctor role"""
    username: str = 'patient123'
    password: str = 'simple_password'
    hashed_password: str = get_password_hash(password=password)
    user = User(username=username, password_hashed=hashed_password)
    db.add(user)
    await db.commit()
    return {'username': username, 'password': password, 'user': user}
