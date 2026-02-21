from celery import Celery

from core.config import settings

celery_app = Celery("worker", broker=settings.redis.url, include=["core.task"])

celery_app.conf.beat_schedule = {
    "generate-fake-report": {
        "task": "core.task.generate_report",
        "schedule": 120.0,
    }
}
celery_app.conf.timezone = "UTC"
