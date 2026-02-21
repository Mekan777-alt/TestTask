from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette_admin import StringField
from starlette_admin.contrib.sqla import ModelView

from core.security import hash_password
from models import Admin


class AdminView(ModelView):
    fields = [
        StringField('login', label='Логин'),
        StringField('password_hash', label='Пароль'),
    ]

    async def create(self, request: Request, data: dict) -> Any:
        if 'password_hash' in data and data['password_hash']:
            plain_password = data['password_hash']
            data['password_hash'] = hash_password(plain_password)
        else:
            raise ValueError("Пароль обязателен для создания администратора.")

        return await super().create(request, data)

    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        session: AsyncSession = request.state.session
        query = await session.execute(select(Admin).where(Admin.id == int(pk)))

        admin = query.scalar()
        if 'password_hash' in data and data['password_hash']:
            plain_password = data['password_hash']
            new_password = hash_password(plain_password)
            data['password_hash'] = new_password
        elif admin:
            data['password_hash'] = admin.password_hash

        return await super().edit(request, pk, data)
