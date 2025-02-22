import asyncio
from datetime import datetime
import torch
import multiprocessing
import base64

import json
from celery import Celery

from app.config import RABBITMQ_URI
from app.ml_models.sentiment_analysis import analyzer
from app.utils.logger import get_logger
from app.db.review_repository import review_repository


class CeleryConfig:
    # Define the queue name
    QUEUE_NAME = "sentiment-analysis"  # Queue for sentiment analysis tasks

    # Celery configuration settings
    CELERY_BROKER_URL = RABBITMQ_URI
    CELERY_RESULT_BACKEND = "rpc://"
    CELERY_TASK_DEFAULT_QUEUE = QUEUE_NAME
    CELERY_TASK_ROUTES = {
        "app.tasks.sentiment-analysis-consumer": {"queue": QUEUE_NAME},
    }


# Initialize Celery app
celery_app = Celery("tasks", broker=RABBITMQ_URI, backend="rpc://")

# Apply the configuration to the Celery app
celery_app.config_from_object(CeleryConfig)

logger = get_logger(__name__)


@celery_app.task(
    bind=True,
    name="sentiment-analysis-consumer",
    queue="sentiment-analysis",
    default_retry_delay=30 * 60,  # Retry after 30 minutes if the task fails
    max_retries=3,  # Maximum number of retries
)
def process_data(self, message):
    try:
        message_data = json.loads(message)
        review_id = message_data["review_id"]
        review_bytes = message_data["review_bytes"]
        review_sentence = base64.b64decode(review_bytes).decode("utf-8")

        print("review", review_sentence)

        today = datetime.today().strftime("%Y-%m-%d")

        prediction = analyzer.predict(review_sentence)

        logger.info(f"prediction: {prediction}")

        with review_repository.sessionmaker() as session:
            review = review_repository.update_review(session, review_id)

            if review:
                match prediction.output:
                    case "POS":
                        review.classification = "positive"
                    case "NEG":
                        review.classification = "negative"
                    case "NEU":
                        review.classification = "neutral"

                review.sentiment_scores = {
                    "positive": round(prediction.probas["POS"], 3),
                    "negative": round(prediction.probas["NEG"], 3),
                    "neutral": round(prediction.probas["NEU"], 3),
                }
                review.classified_at = today
                review.classified = True
                session.commit()

            else:
                logger.warning(f"Review with id {review_id} not found")

        logger.info(f"Prediction for id {review_id} completed successfully.")
    except Exception as exc:
        error = str(exc)
        logger.error(f"Error occurred: {error}")
        self.retry(exc=exc)
