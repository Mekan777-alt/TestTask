from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette_admin import DateTimeField, EnumField, IntegerField, StringField
from starlette_admin.contrib.sqla import ModelView

from core.security import hash_password
from models.user import User

STATUS_CHOICES = [
      ("active", "Активный"),
      ("inactive", "Неактивный"),
      ("blocked", "Заблокирован"),
  ]


class UserView(ModelView):
    fields = [
        IntegerField("id", label="ID"),
        StringField("email", label="Почта"),
        StringField("password_hash", label="Пароль"),
        EnumField("status", choices=STATUS_CHOICES, select2=False, label="Статус"),
        DateTimeField("last_login_at", label="Последний вход"),
        DateTimeField("created_at", label="Дата создания"),
        DateTimeField("updated_at", label="Дата обновления"),
    ]
    exclude_fields_from_create = ["id", "last_login_at", "created_at", "updated_at"]
    exclude_fields_from_edit = ["id", "created_at", "updated_at"]

    async def create(self, request: Request, data: dict) -> Any:
        if data.get("password_hash"):
            data["password_hash"] = hash_password(data["password_hash"])
        return await super().create(request, data)

    async def edit(self, request: Request, pk: Any, data: dict) -> Any:
        if data.get("password_hash"):
            data["password_hash"] = hash_password(data["password_hash"])
        else:
            session: AsyncSession = request.state.session
            result = await session.execute(select(User).where(User.id == int(pk)))
            user = result.scalar()
            if user:
                data["password_hash"] = user.password_hash
        return await super().edit(request, pk, data)
