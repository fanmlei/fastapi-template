from celery import Celery

from src.core.config import settings

celery_app = Celery("mlinks", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND, include=[])

celery_app.conf.update(
    task_serializer="pickle",
    accept_content=["pickle", "json"],
    result_serializer="pickle",
    timezone="Asia/Shanghai",
    enable_utc=True,
    task_result_expires=3600,
    task_time_limit=300,
)

celery_app.conf.beat_schedule = {
    # "beat-30-seconds": {
    #     "task": "src.tasks.beat_task.add",
    #     "schedule": 30.0,
    #     "args": (16, 16),
    # },
}

# worker
# celery -A src.tasks.celery_app worker -l INFO

# beat
# celery -A src.tasks.celery_app beat -l INFO
