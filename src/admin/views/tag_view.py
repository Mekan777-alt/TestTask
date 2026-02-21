from starlette_admin import IntegerField, StringField
from starlette_admin.contrib.sqla import ModelView


class TagView(ModelView):
    fields = [
        IntegerField("id", label="ID"),
        StringField('name', label="Название")
    ]
