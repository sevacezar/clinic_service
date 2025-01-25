"""Module with auth fastapi dependencies"""

from datetime import datetime, timezone

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dao import UsersDAO
from auth.models import User
from config import JWT_ALGORITHM, JWT_SECRET
from dependencies import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session),
    ) -> User:
    """Get user using token data"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid!')
    
    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is expired!')
    
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User ID is not found!')
        
    user: User | None = await UsersDAO.get_user_by_id(session=session, id=int(id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User is not found')
    
    return user

async def get_current_doctor_user(
        current_user: User = Depends(get_current_user),
) -> User:
    """Get user if has doctor role"""
    if current_user.role.name != 'doctor':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Forbidden!')
    return current_user
