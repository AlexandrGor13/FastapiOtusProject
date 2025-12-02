"""Add admin

Revision ID: e4fbe212603b
Revises: e14ec97473a7
Create Date: 2025-11-18 21:46:37.062851

"""
from typing import Sequence, Union

from alembic import op

from core.config import settings
from core.security import get_password_hash


# revision identifiers, used by Alembic.
revision: str = 'e4fbe212603b'
down_revision: Union[str, None] = 'e14ec97473a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем нового пользователя
    op.execute(
        f"""
        INSERT INTO users (username, email, password_hash, role)
        VALUES ('{settings.admin.user}', 'admin', '{get_password_hash(settings.admin.password)}', 'admins');
        """
    )


def downgrade() -> None:
    # Удаляем нового пользователя
    op.execute("DELETE FROM users WHERE username = 'admin';")
