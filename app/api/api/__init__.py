from .users import router as users_router
from .profiles import router as profile_router
from .image import router as image_router

from fastapi import APIRouter

router = APIRouter( )

router.include_router(users_router)
router.include_router(profile_router)
router.include_router(image_router)