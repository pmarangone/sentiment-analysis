from celery import Celery

from app.config import RABBITMQ_URI

# TODO: configure queue name

celery_app = Celery("tasks", broker=RABBITMQ_URI, backend="rpc://")
