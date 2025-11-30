from auth import router as auth_router
from api.users import router as users_router
from api.profiles import router as profile_router
from api.image import router as image_router

from fastapi import APIRouter

router = APIRouter( )

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(profile_router)
router.include_router(image_router)
