"""Module with fastapi views of auth"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import verify_password, create_access_token
from auth.dao import UsersDAO
from auth.models import User
from auth.schemas import LoginPydanticIn, LoginPydanticOut
from dependencies import get_session


router: APIRouter = APIRouter(prefix='', tags=['Auth'])


@router.post('/login', response_model=LoginPydanticOut)
async def login(
    login_data: LoginPydanticIn,
    session: AsyncSession = Depends(get_session)
):
    """Get token if auth is success"""
    user: User | None = await UsersDAO.get_user_by_username(
        session=session,
        username=login_data.username,
    )
    if not user or not verify_password(login_data.password, user.password_hashed):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials!'
        )
    
    token: str = create_access_token(data={'sub': str(user.id)})
    return {'token': token}
    