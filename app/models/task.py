from typing import TYPE_CHECKING
from enum import Enum
from datetime import date

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .project import Project


class Status(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class Priority(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = None
    status: Status = Field(default=Status.NEW)
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: date = Field(index=True)
    
    project_id: int = Field(foreign_key='project.id', ondelete='CASCADE')
    project: "Project" = Relationship(back_populates='tasks')