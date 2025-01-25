"""Module with auth functions"""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from config import JWT_SECRET, JWT_ALGORITHM, EXPIRES_DELTA_DAYS


pwd_context = CryptContext(schemes=['bcypt'], deprecated='auto')

def get_password_hash(password: str) -> str:
    """Get hash of password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare password and hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(days=EXPIRES_DELTA_DAYS)
    ) -> str:
    """Create JWT-token"""
    to_encode: dict = data.copy()
    expire = datetime.now(timezone=timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, JWT_SECRET, JWT_ALGORITHM)

