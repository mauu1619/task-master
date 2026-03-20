from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

from app.core.config import settings
from app.db.session import get_session
from app.models.user import User

class Token(BaseModel):
    access_token: str
    token_type: str


password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash('dummypassword')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/login/token')


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def authenticate_user(
    session: Annotated[Session, Depends(get_session)],
    username: str,
    password: str
):
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise credentials_exception
    return user