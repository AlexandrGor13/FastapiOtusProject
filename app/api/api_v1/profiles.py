from typing import Annotated
from fastapi import APIRouter, Body, status, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.exc import NoResultFound, InterfaceError

from crud.profile import ProfileCRUD, profile_crud
from core.schemas.profile import ProfileRead, default_profile
from dependencies.dependencies import get_current_user

router = APIRouter(tags=["Profile"], prefix="/api/users")


@router.get(
    "/me/profile",
    status_code=status.HTTP_200_OK,
    summary="Get user info",
    responses={
        status.HTTP_200_OK: {
            "description": "User info",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User info",
                        "user info": {},
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    },
)
async def my_profile(
    current_user: Annotated[str, Depends(get_current_user)],
    crud: Annotated[ProfileCRUD, Depends(profile_crud)],
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
    try:
        profile = await crud.get_by_name(current_user)
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    return {
        "description": "User info",
        "user info": profile,
    }


#
@router.put(
    "/me/profile",
    status_code=status.HTTP_200_OK,
    summary="Update user",
    responses={
        status.HTTP_200_OK: {
            "description": "User updated",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User updated",
                        "user info": {},
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    },
)
async def update_my_profile(
    current_user: Annotated[str, Depends(get_current_user)],
    crud: Annotated[ProfileCRUD, Depends(profile_crud)],
    profile_in: Annotated[ProfileRead, Body()] = default_profile,
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы можем изменить информацию о пользователе.
    """
    try:
        profile = await crud.update(current_user, profile_in)
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    return {
        "description": "User updated",
        "user info": profile,
    }


@router.get(
    "/profiles",
    status_code=status.HTTP_200_OK,
)
async def all_profiles(
    crud: Annotated[ProfileCRUD, Depends(profile_crud)],
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
    try:
        users = await crud.get()
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    return users
