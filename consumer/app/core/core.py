import base64
import json

from aio_pika import IncomingMessage

from app.ml_models.sentiment_analysis import analyzer
from app.config import MAX_RETRIES
from app.db.review_repository import review_repository
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def predict_sentiment(message: IncomingMessage):
    try:
        message_data = json.loads(message.body.decode("utf-8"))

        print("message_data", message_data)

        review_id = message_data["review_id"]
        review_bytes = message_data["review_bytes"]
        review = base64.b64decode(review_bytes).decode("utf-8")

        print("review", review)

        transcription = analyzer.predict(review)

        with review_repository.sessionmaker() as session:
            review_repository.update_review(session, review_id, transcription)
            session.commit()

        logger.info(f"Task {review_id} completed successfully.")

    except Exception as exc:
        logger.error(f"Task failed: {exc}")

        headers = message.headers or {}
        retry_count = headers.get("x-retry-count", 0)

        if retry_count < MAX_RETRIES:
            headers["x-retry-count"] = retry_count + 1

            await message.nack(requeue=True)

            logger.info(f"Requeued message (retry {retry_count + 1}/{MAX_RETRIES})")
        else:
            await message.nack(requeue=False)

            logger.error(f"Retry limit exceeded for message: {message.body.decode()}")
        raise exc
