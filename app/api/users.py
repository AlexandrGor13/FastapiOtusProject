from typing import Annotated
from fastapi import APIRouter, Body, status, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.exc import NoResultFound, InterfaceError, IntegrityError

from crud.user import UsersCRUD, users_crud
from core.schemas.user import User as UserSchema, default_user
from dependencies.dependencies import get_current_user, get_current_admin
from crud.profile import ProfileCRUD, profile_crud
from core.schemas.profile import ProfileRead, default_profile

router = APIRouter(tags=["Users"], prefix="/api/users")


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Create user",
    responses={
        status.HTTP_200_OK: {
            "description": "User created",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User created",
                        "user info": {
                            "username": "string",
                            "email": "user@example.com",
                        },
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {"description": "User already exists"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    },
)
async def set_user(
    crud_user: Annotated[UsersCRUD, Depends(users_crud)],
    crud_profile: Annotated[ProfileCRUD, Depends(profile_crud)],
    user_in: Annotated[UserSchema, Body()] = default_user,
    profile_in: Annotated[ProfileRead, Body()] = default_profile,
):
    """
    Создание нового пользователя
    """
    try:
        user = await crud_user.create(user_in)
        profile = await crud_profile.create(user_in.username, profile_in)
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    except IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "User already exists"},
        )
    return {"description": "User created", "user info": user, "profile": profile}


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get user info",
    responses={
        status.HTTP_200_OK: {
            "description": "User info",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User info",
                        "user info": {
                            "username": "string",
                            "email": "user@example.com",
                        },
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
async def about_me(
    current_user: Annotated[dict, Depends(get_current_user)],
    crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
    try:
        user = await crud.get_by_name(current_user.get("username"))
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
        "user info": user,
    }


@router.put(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Update user",
    responses={
        status.HTTP_200_OK: {
            "description": "User updated",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User updated",
                        "user info": {
                            "username": "string",
                            "email": "user@example.com",
                        },
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
async def update_user_info(
    current_user: Annotated[dict, Depends(get_current_user)],
    crud: Annotated[UsersCRUD, Depends(users_crud)],
    user_in: Annotated[UserSchema, Body()] = default_user,
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы можем изменить информацию о пользователе.
    """
    try:
        user = await crud.update(current_user.get("username"), user_in)
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
        "user info": user,
    }


@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Delete user",
    responses={
        status.HTTP_200_OK: {
            "description": "User deleted",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User deleted",
                        "user info": {
                            "username": "string",
                            "email": "user@example.com",
                        },
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
async def del_user(
    current_user: Annotated[dict, Depends(get_current_user)],
    crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы можем удалить пользователя.
    """
    try:
        user = await crud.delete(current_user.get("username"))
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    return JSONResponse(
        content={
            "detail": "User deleted",
            "user info": user,
        }
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_admin)],
)
async def all_users(
    crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Этот маршрут защищен и требует токен администратора.
    Если токен действителен, мы возвращаем информацию о всех пользователях.
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
