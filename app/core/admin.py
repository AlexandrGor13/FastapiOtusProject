from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
import uuid
from api import router
from core.models.base import async_session
from core.models.user import RoleEnum
from core.security import verify_password
from core.models import (
    User,
    Profile,
    async_engine,
)
from crud.user import UsersCRUD


def create_admin_panel(app: FastAPI):
    app.include_router(router)
    admin = Admin(
        app,
        async_engine,
        authentication_backend=authentication_backend,
        base_url="/adminka",
    )
    admin.add_view(UserAdmin)
    admin.add_view(ProfileAdmin)


class UserAdmin(ModelView, model=User):
    column_list = User.get_columns()


class ProfileAdmin(ModelView, model=Profile):
    column_list = Profile.get_columns()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        is_pass_ok = False
        is_role_ok = False
        async with async_session() as session:
            crud = UsersCRUD(session)
            user = await crud.get_by_name(username)
            if user:
                role = await crud.get_role_by_name(username)
                hash_pw = await crud.get_hash_by_name(username)
                is_pass_ok = verify_password(password, hash_pw)
                is_role_ok = role == RoleEnum.admins
        if not (is_pass_ok and is_role_ok):
            return False
        # And update session
        request.session.update({"token": str(uuid.uuid4())})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key=str(uuid.uuid4()))
