from datetime import datetime
import base64
import json

from app.core import get_prediction, get_prediction_next
from app.ml_models.sentiment_analysis import get_analyzer
from app.utils.logger import get_logger
from app.db.review_repository import get_review_repository

logger = get_logger(__name__)


def process_review(message):
    analyzer = get_analyzer()
    review_repository = get_review_repository()

    message_data = json.loads(message)
    review_id = message_data["review_id"]
    review_bytes = message_data["review_bytes"]
    review_sentence = base64.b64decode(review_bytes).decode("utf-8")

    today = datetime.today().strftime("%Y-%m-%d")

    prediction = analyzer.predict(review_sentence)[0]

    logger.info(f"prediction: {prediction}")

    with review_repository.sessionmaker() as session:
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

        else:
            logger.warning(f"Review with id {review_id} not found")

    logger.info(f"Prediction for id {review_id} completed successfully.")
