from typing import Annotated
from fastapi import APIRouter, Body, status, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.exc import NoResultFound, InterfaceError

from app.crud.profile import ProfileCRUD, profile_crud
from app.core.schemas.profile import ProfileRead, default_profile
from app.dependencies.dependencies import get_current_user, get_current_admin

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
    current_user: Annotated[dict, Depends(get_current_user)],
    crud: Annotated[ProfileCRUD, Depends(profile_crud)],
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем профиль пользователя.
    """
    try:
        profile = await crud.get_by_name(current_user.get("username"))
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
    current_user: Annotated[dict, Depends(get_current_user)],
    crud: Annotated[ProfileCRUD, Depends(profile_crud)],
    profile_in: Annotated[ProfileRead, Body()] = default_profile,
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы можем изменить профиль пользователя.
    """
    try:
        profile = await crud.update(current_user.get("username"), profile_in)
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
    dependencies=[Depends(get_current_admin)],
)
async def all_profiles(
    crud: Annotated[ProfileCRUD, Depends(profile_crud)],
):
    """
    Этот маршрут защищен и требует токен администратора. Если токен действителен, мы возвращаем профили всех пользователей.
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
