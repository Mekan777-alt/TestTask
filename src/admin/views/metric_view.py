from starlette_admin import DateTimeField, HasMany, IntegerField, StringField, TextAreaField
from starlette_admin.contrib.sqla import ModelView


class MetricView(ModelView):
    fields = [
        IntegerField("id", label="ID"),
        StringField("name", label="Название"),
        TextAreaField("description", label="Описание"),
        IntegerField("owner_id", label="Владелец"),
        DateTimeField("created_at", label="Дата создания"),
        HasMany("records", label="Записи"),
    ]

    exclude_fields_from_create = ["id", "created_at"]
    exclude_fields_from_edit = ["id", "created_at"]
    searchable_fields = ["name"]
