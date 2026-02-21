from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine, func, select

from celery_app import celery_app
from core.config import settings

REPORTS_DIR = Path(__file__).resolve().parent.parent.parent / "reports"


@celery_app.task(name="core.task.generate_report")
def generate_report():
    from models.metric import Metric
    from models.metric_record import MetricRecord

    engine = create_engine(settings.database.sync_url)

    with engine.connect() as connection:
        metrics_count = connection.execute(select(func.count(Metric.id))).scalar()
        records_count = connection.execute(select(func.count(MetricRecord.id))).scalar()

    engine.dispose()

    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / "report.txt"
    report_path.write_text(
        f"Отчет от {datetime.now():%Y-%m-%d %H:%M:%S}\n"
        f"Количество метрик: {metrics_count}\n"
        f"Количество записей: {records_count}\n"
    )
