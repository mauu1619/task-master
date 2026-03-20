from typing import Annotated, Sequence

from fastapi import Depends, APIRouter, HTTPException, status, Query, Path
from sqlmodel import Session, select

from app.schemas.tasks import TaskCreate, TaskFilters, TaskUpdate
from app.db.session import get_session
from app.models.task import Task
from app.models.user import User
from app.models.project import Project
from app.core.security import get_current_user


router = APIRouter()


def get_task_or_error(
    *,
    project_id: Annotated[int, Query(ge=0)],
    task_id: Annotated[int, Path(ge=0)],
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task.project.owner_id != user.id or task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return task


@router.post("/", response_model=Task)
async def create_task(
    *,
    task_in: TaskCreate,
    project_id: Annotated[int, Query(ge=0)],
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
):
    for project in user.projects:
        if project_id == project.id:
            break
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    db_task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        priority=task_in.priority,
        due_date=task_in.due_date,
        project_id=project_id
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/")
async def get_tasks(
    *,
    project_id: Annotated[int, Query(ge=0)],
    filter_by: Annotated[TaskFilters, Depends()],
    session: Annotated[Session, Depends(get_session)],
    user: Annotated[User, Depends(get_current_user)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=5)] = 5
):
    statement = select(Task).join(Project).where(
        project_id == Task.project_id).where(Project.owner_id == user.id)

    if filter_by.priority:
        statement = statement.where(Task.priority == filter_by.priority)
    if filter_by.status:
        statement = statement.where(Task.status == filter_by.status)

    tasks = session.exec(statement.offset(offset).limit(limit)).all()

    return tasks


@router.patch("/{task_id}")
async def update_task(
    task_update: TaskUpdate,
    db_task: Annotated[Task, Depends(get_task_or_error)],
    session: Annotated[Session, Depends(get_session)]
):
    updated_data = task_update.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/{task_id}")
async def get_task(
    db_task: Annotated[Task, Depends(get_task_or_error)]
) -> Task:
    return db_task


@router.delete("/{task_id}")
async def delete_task(
    db_task: Annotated[Task, Depends(get_task_or_error)],
    session: Annotated[Session, Depends(get_session)]
):
    session.delete(db_task)
    session.commit()

    return {"OK": True}