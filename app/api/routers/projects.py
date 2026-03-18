from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException, status, Query
from sqlmodel import Session, select

from app.core.security import get_session, get_current_user
from app.models.project import Project
from app.models.user import User
from app.schemas.projects import ProjectCreate, ProjectUpdate


router = APIRouter()

 
def get_project_or_error(
    *,
    project_id: Annotated[int, Path(ge=0)],
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)]
) -> Project:
    project = session.get(Project, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return project
    


@router.post("/", response_model=Project)
async def create_project(
    *,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    project: ProjectCreate
):
    db_project = Project(
        title=project.title,
        description=project.description,
        owner_id=user.id
    )
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    
    return db_project


@router.get("/")
async def get_projects(
    *,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=5)] = 5
):
    projects = session.exec(
        select(Project).where(
            user.id == Project.owner_id).offset(offset).limit(limit)).all()
    if not projects:
        return {"message": "There is no projects yet"}
    return projects


@router.get("/{project_id}")
async def get_project(
    *,
    db_project: Annotated[Project, Depends(get_project_or_error)]
):
    return db_project

@router.patch("/{project_id}", response_model=Project)
async def update_project(
    *,
    db_project: Annotated[Project, Depends(get_project_or_error)],
    session: Annotated[Session, Depends(get_session)],
    project_in: ProjectUpdate
):
    updated_data = project_in.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        setattr(db_project, key, value)

    session.add(db_project)
    session.commit()
    session.refresh(db_project)

    return db_project
    

@router.delete("/{project_id}")
async def delete_project(
    *,
    db_project: Annotated[Project, Depends(get_project_or_error)],
    session: Annotated[Session, Depends(get_session)]
):
    session.delete(db_project)
    session.commit()
    
    return {"OK": True}