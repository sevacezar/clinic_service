"""Module with auth fastapi dependencies"""

from fastapi.security import OAuth2PasswordBearer

aouth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

