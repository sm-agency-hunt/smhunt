"""
Celery configuration for SMHunt
"""
from celery import Celery


# Initialize Celery app
celery_app = Celery('smhunt')

# Configure Celery
celery_app.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@celery_app.task
def example_task(data):
    """
    Example background task
    """
    # TODO: Implement actual task logic
    return {"status": "completed", "data": data}
