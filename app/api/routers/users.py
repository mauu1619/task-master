from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter, status
from sqlmodel import Session, select

from app.models.user import User
from app.schemas.user import UserCreate, UserShow
from app.db.session import get_session
from app.core.security import get_password_hash, get_current_user


router = APIRouter()


@router.post("/register", response_model=UserShow, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: Annotated[Session, Depends(get_session)]
):
    existing_user = session.exec(select(User).where(User.username == user_in.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    db_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password)
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=UserShow)
async def who_am_i(
    user: Annotated[User, Depends(get_current_user)]
):
    return user 