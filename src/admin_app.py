import models
from admin import views
from database.session import async_session
from sqlalchemy import select
from starlette.applications import Starlette
from starlette_admin.contrib.sqla import ModelView
from database.session import engine
from starlette_admin.contrib.sqla import Admin
from starlette_admin import I18nConfig
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from admin.auth.provider import AdminAuthProvider
from core.config import settings
from core.security import hash_password


async def initialize_admin():
    async with async_session() as session:
        result = await session.execute(select(models.Admin).where(models.Admin.login == "admin"))
        model_admin = result.scalar_one_or_none()

        if not model_admin:
            default_admin = models.Admin(login="admin", password_hash=hash_password("admin123"))
            session.add(default_admin)
            await session.commit()

i18n_config = I18nConfig(default_locale="ru")

app = Starlette(on_startup=[initialize_admin])

admin = Admin(engine,
              title="Админка",
              base_url="/admin",
              auth_provider=AdminAuthProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key=settings.jwt.secret_key)],
              i18n_config=i18n_config
              )


admin.add_view(views.AdminView(models.Admin, icon="fa fa-users", label="Администраторы"))
admin.add_view(views.UserView(models.User, icon="fa fa-users", label="Пользователи"))
admin.add_view(views.TagView(models.Tag, icon="fa fa-tag", label="Теги"))
admin.add_view(views.MetricView(models.Metric, icon="fa fa-chart-line", label="Метрики"))
admin.add_view(views.MetricRecordView(models.MetricRecord, icon="fa fa-list", label="Записи метрик"))

admin.mount_to(app)