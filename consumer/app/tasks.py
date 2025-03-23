from app.core.process_many_reviews import process_many_reviews
from app.core.process_single_review import process_review
from app.utils.logger import get_logger
from app import celery_app

logger = get_logger(__name__)


@celery_app.task(
    bind=True,
    name="sentiment-analysis-consumer",
    queue="sentiment-analysis",
    default_retry_delay=30 * 60,  # Retry after 30 minutes if the task fails
    max_retries=3,  # Maximum number of retries
)
def task_process_review(self, message):
    try:
        process_review(message)

    except Exception as exc:
        logger.error(f"Error occurred when processing single review: {str(exc)}")
        self.retry(exc=exc)


@celery_app.task(
    bind=True,
    name="sentiment-analysis-consumer-many",
    queue="sentiment-analysis",
    default_retry_delay=30 * 60,
    max_retries=3,
)
def task_process_many(self, message):
    try:
        process_many_reviews(message)

    except Exception as exc:
        logger.error(f"Error occurred when processing many reviews: {str(exc)}")
        self.retry(exc=exc)
