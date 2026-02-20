from starlette_admin.contrib.sqla import ModelView
from starlette_admin import StringField, IntegerField, EmailField, EnumField, DateTimeField

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
    exclude_fields_from_create = ["last_login_at", "created_at", "updated_at"]
    exclude_fields_from_edit = ["created_at", "updated_at"]