from fastapi import APIRouter

from .auth import router as auth_router
from .celery_tasks import router as celery_tasks_router
from .trips import router as trips_router

router = APIRouter()

router.include_router(router=auth_router)
router.include_router(router=trips_router)
router.include_router(router=celery_tasks_router)
