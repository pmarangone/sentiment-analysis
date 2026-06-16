from datetime import datetime
import base64
import json
import traceback

from app.core import get_prediction, get_prediction_next
from app.ml_models.sentiment_analysis import get_analyzer
from app.utils.logger import get_logger
from app.db.review_repository import get_review_repository

logger = get_logger(__name__)


def process_review(message):
    try:
        analyzer = get_analyzer()
    except Exception as e:
        logger.error(f"Failed to initialize analyzer: {e}")
        raise e

    review_repository = get_review_repository()

    try:
        message_data = json.loads(message)
        review_id = message_data["review_id"]
        review_bytes = message_data["review_bytes"]
        review_sentence = base64.b64decode(review_bytes).decode("utf-8")
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.error(f"Failed to parse message: {e}")
        return

    today = datetime.today().strftime("%Y-%m-%d")

    try:
        prediction = analyzer.predict(review_sentence)[0]
    except Exception as e:
        logger.error(f"Failed to predict sentiment for id {review_id}: {e}")
        raise e

    with review_repository.sessionmaker() as session:
        try:
            review = review_repository.update_review(session, review_id)

            if review:
                review.classification = get_prediction(prediction)

                review.sentiment_scores = {
                    "positive": round(get_prediction_next(prediction, "POS"), 3),
                    "negative": round(get_prediction_next(prediction, "NEG"), 3),
                    "neutral": round(get_prediction_next(prediction, "NEU"), 3),
                }
                review.classified_at = today
                review.classified = True
                session.commit()
                logger.info(f"Prediction for id {review_id} completed successfully.")
            else:
                logger.warning(f"Review with id {review_id} not found")
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update database for id {review_id}: {e}\n{traceback.format_exc()}")
            raise e
