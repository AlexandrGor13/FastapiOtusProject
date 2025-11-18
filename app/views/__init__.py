from .root import router as root_router
from fastapi import APIRouter

router = APIRouter( )

router.include_router(root_router)