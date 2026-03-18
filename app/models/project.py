from typing import TYPE_CHECKING
from datetime import date

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .task import Task


class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = None
    created_at: date | None = Field(default=date.today(), index=True)
    
    owner_id: int | None = Field(foreign_key='user.id', ondelete='CASCADE')
    owner: "User" = Relationship(back_populates='projects')

    tasks: list["Task"] = Relationship(back_populates='project', passive_deletes='all')