"""Module with auth fastapi dependencies"""

from datetime import datetime, timezone

from fastapi import Depends, status, HTTPException, Header
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dao import UsersDAO
from auth.models import User
from config import JWT_ALGORITHM, JWT_SECRET
from dependencies import get_session


async def get_token_from_header(authorization: str = Header(default=None)) -> str:
    """Get token form header"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Missing Authorization header!',
        )
    if not authorization.startswith('Bearer '):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid Authorization header!',
        )
    return authorization[len('Bearer '):]

async def get_current_user(
        token: str = Depends(get_token_from_header),
        session: AsyncSession = Depends(get_session),
    ) -> User:
    """Get user using token data"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired!')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')
    
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID is not found!')
    
    try:
        user_id: int = int(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID is invalid!')

    user: User | None = await UsersDAO.get_user_by_id(session=session, id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not found!')
    
    return user

async def get_current_doctor_user(
        current_user: User = Depends(get_current_user),
) -> User:
    """Get user if has doctor role"""
    if not current_user.role or current_user.role.name != 'doctor':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden!')
    return current_user
