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

# Configure Celery to use RabbitMQ as a broker
celery = Celery("tasks", broker=RABBITMQ_URI, backend="rpc://")


logger = get_logger(__name__)


@celery.task
def process_data(message):
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
