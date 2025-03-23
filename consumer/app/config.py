import os

REDIS_HOST = os.environ.get("REDIS_HOST")
RABBITMQ_URI = os.environ.get("RABBITMQ_URI")
POOL_SIZE = os.environ.get("POOL_SIZE")
MAX_RETRIES = os.environ.get("MAX_RETRIES")
DATABASE_URL = os.environ.get("DATABASE_URL")


class CeleryConfig:
    # Define the queue name
    QUEUE_NAME = "sentiment-analysis"  # Queue for sentiment analysis tasks

    # Celery configuration settings
    CELERY_BROKER_URL = RABBITMQ_URI
    CELERY_RESULT_BACKEND = "rpc://"
    CELERY_TASK_DEFAULT_QUEUE = QUEUE_NAME
    CELERY_TASK_ROUTES = {
        "app.tasks.sentiment-analysis-consumer": {"queue": QUEUE_NAME},
        "app.tasks.sentiment-analysis-consumer-many": {"queue": QUEUE_NAME},
    }
