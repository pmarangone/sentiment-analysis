from celery import Celery

from app.config import RABBITMQ_URI


class CeleryConfig:
    # Define the queue name
    QUEUE_NAME = "sentiment-analysis"  # Replace with your desired queue name

    # Celery configuration settings
    CELERY_BROKER_URL = RABBITMQ_URI
    CELERY_RESULT_BACKEND = "rpc://"
    CELERY_TASK_DEFAULT_QUEUE = QUEUE_NAME
    CELERY_TASK_ROUTES = {
        # "app.tasks.task_name": {"queue": "specific_queue"},
    }


celery_app = Celery("tasks", broker=RABBITMQ_URI, backend="rpc://")

celery_app.config_from_object(CeleryConfig)
