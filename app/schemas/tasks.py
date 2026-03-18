from datetime import date

from pydantic import BaseModel
from fastapi import Query
from app.models.task import Status, Priority


class TaskCreate(BaseModel):
    title: str 
    description: str | None = None
    status: Status
    priority: Priority
    due_date: date


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: Status | None = None
    priority: Priority | None = None
    due_date: date | None = None


class TaskFilters(BaseModel):
    status: Status | None = Query(None, description="Filter by tasks' status")
    priority: Priority | None = Query(None, description="Filter by tasks' priority")