from datetime import datetime
import base64
import json

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
