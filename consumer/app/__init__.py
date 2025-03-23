from app.utils.logger import get_logger
from celery import Celery

from app.config import RABBITMQ_URI, CeleryConfig

logger = get_logger(__name__)

# Initialize Celery app
celery_app = Celery("tasks", broker=RABBITMQ_URI, backend="rpc://")

# Apply the configuration to the Celery app
celery_app.config_from_object(CeleryConfig)

# Setup the tasks file
celery_app.autodiscover_tasks(["app.tasks"])

logger.info("Celery worker module loaded.")
