from fastapi import APIRouter

from app.api.routers import login_router, task_router, user_router, project_router


router = APIRouter()


router.include_router(login_router, prefix="/login", tags=['user'])
router.include_router(project_router, prefix="/projects", tags=['projects'])
router.include_router(task_router, prefix="/tasks", tags=['tasks'])
router.include_router(user_router, prefix="/user", tags=['user'])