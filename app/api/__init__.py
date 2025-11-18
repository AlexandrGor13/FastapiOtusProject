from .auth import router as auth_router
from .api_v1 import router as api_v1_router

from fastapi import APIRouter

router = APIRouter( )

router.include_router(auth_router)
router.include_router(api_v1_router)
