from typing import TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr

if TYPE_CHECKING:
    from .project import Project


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: EmailStr | None = None
    hashed_password: str

    projects: list['Project'] = Relationship(back_populates='owner', passive_deletes='all')