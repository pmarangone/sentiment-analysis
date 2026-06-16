from datetime import datetime
import base64
import json
import traceback

from app.core import get_prediction, get_prediction_next
from app.ml_models.sentiment_analysis import get_analyzer
from app.utils.logger import get_logger
from app.db.review_repository import get_review_repository

logger = get_logger(__name__)


def process_many_reviews(message):
    try:
        analyzer = get_analyzer()
    except Exception as e:
        logger.error(f"Failed to initialize analyzer: {e}")
        raise e

    review_repository = get_review_repository()

    try:
        data = json.loads(message)
    except Exception as e:
        logger.error(f"Failed to parse batch message: {e}")
        return

    today = datetime.today().strftime("%Y-%m-%d")

    try:
        review_ids = [message_data["review_id"] for message_data in data]
        reviews = [
            base64.b64decode(message_data["review_bytes"]).decode("utf-8")
            for message_data in data
        ]
    except KeyError as e:
        logger.error(f"Missing key in batch message: {e}")
        return

    logger.info(f"Processing {len(review_ids)} reviews")
    
    try:
        predictions = analyzer.predict(reviews)
    except Exception as e:
        logger.error(f"Failed to predict batch sentiment: {e}")
        raise e

    reviews_to_update = [
        {
            "id": review_id,
            "classification": get_prediction(prediction),
            "sentiment_scores": {
                "positive": round(get_prediction_next(prediction, "POS"), 3),
                "negative": round(get_prediction_next(prediction, "NEG"), 3),
                "neutral": round(get_prediction_next(prediction, "NEU"), 3),
            },
            "classified_at": today,
            "classified": True,
        }
        for review_id, prediction in zip(review_ids, predictions)
    ]

    if reviews_to_update:
        Session = review_repository.sessionmaker
        session = Session()

        try:
            review_repository.bulk_update_reviews(session, reviews_to_update)
            session.commit()
            logger.info(f"Bulk update completed for {len(reviews_to_update)} reviews.")

        except Exception as exc:
            session.rollback()
            logger.error(f"Bulk update failed: {str(exc)}\n{traceback.format_exc()}.")
            raise exc

        finally:
            session.close()
