from fastapi import APIRouter
from .todos import router as todo_router
from .columns import router as columns_router
from .projects import router as projects_router
from .comments import router as comments_router
from .todo_timers import router as todo_timer_router
from .tasks import router as task_router
from .progress_indicator import router as progress_indicator

from .triggers import router as trigger_router


router = APIRouter()

todo_router.include_router(
    comments_router,
    prefix="/{todo_id}/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

todo_router.include_router(
    todo_timer_router,
    prefix="/{todo_id}/todo_timer",
    tags=["todo timer"],
    responses={404: {"description": "Not found"}},
)


todo_router.include_router(
    task_router,
    prefix="/{todo_id}/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    todo_router,
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    columns_router,
    prefix="/columns",
    tags=["columns"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    projects_router,
    prefix="/projects",
    tags=["project"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    trigger_router,
    prefix="/triggers",
    tags=["triggers"],
    responses={404: {"description": "Not found"}},
)

router.include_router(
    progress_indicator,
    prefix="/progress_indicator",
    tags=["progress_indicator"],
    responses={404: {"description": "Not found"}},
)