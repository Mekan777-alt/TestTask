from starlette_admin import DateTimeField, FloatField, IntegerField
from starlette_admin.contrib.sqla import ModelView


class MetricRecordView(ModelView):
    fields = [
        IntegerField("id", label="ID"),
        IntegerField("metric_id", label="Метрика"),
        FloatField("value", label="Значение"),
        DateTimeField("timestamp", label="Время измерения"),
        DateTimeField("created_at", label="Дата создания"),
    ]

    exclude_fields_from_create = ["id", "created_at"]
    exclude_fields_from_edit = ["id", "created_at"]
    searchable_fields = ["metric_id"]
