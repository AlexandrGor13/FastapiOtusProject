from app.api.root import router as root_router
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.profiles import router as profile_router
from app.api.image import router as image_router

from fastapi import APIRouter

router = APIRouter()

router.include_router(root_router)
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(profile_router)
router.include_router(image_router)
