"""Module with Pydantic-schemas of auth"""

from pydantic import BaseModel


class LoginPydanticIn(BaseModel):
    """Input auth scheme"""
    username: str
    password: str


class LoginPydanticOut(BaseModel):
    """Output auth scheme"""
    token: str

