from datetime import datetime
import base64
import json

from app.ml_models.sentiment_analysis import get_analyzer
from app.utils.logger import get_logger
from app.db.review_repository import get_review_repository

logger = get_logger(__name__)


def process_many_reviews(message):
    analyzer = get_analyzer()
    review_repository = get_review_repository()

    logger.info("Processing multiple reviews")
    data = json.loads(message)
    today = datetime.today().strftime("%Y-%m-%d")

    reviews_to_update = []

    for message_data in data:
        review_id = message_data["review_id"]
        review_bytes = message_data["review_bytes"]
        review_sentence = base64.b64decode(review_bytes).decode("utf-8")

        prediction = analyzer.predict(review_sentence)
        logger.info(f"Prediction for review {review_id}: {prediction}")

        review_update = {
            "id": review_id,
            "classification": prediction.output,
            "sentiment_scores": {
                "positive": round(prediction.probas["POS"], 3),
                "negative": round(prediction.probas["NEG"], 3),
                "neutral": round(prediction.probas["NEU"], 3),
            },
            "classified_at": today,
            "classified": True,
        }
        reviews_to_update.append(review_update)

    if reviews_to_update:
        Session = review_repository.sessionmaker
        session = Session()

        try:
            review_repository.bulk_update_reviews(session, reviews_to_update)
            session.commit()
            logger.info(f"Bulk update completed for {len(reviews_to_update)} reviews.")

        except Exception as exc:
            logger.error(f"Bulk update failed {str(exc)}.")
            raise exc

        finally:
            session.close()
