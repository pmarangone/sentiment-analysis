import base64
import json
from datetime import datetime
from aio_pika import IncomingMessage

from app.ml_models.sentiment_analysis import analyzer
from app.config import MAX_RETRIES
from app.db.review_repository import review_repository
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def predict_sentiment(message: IncomingMessage):
    """
    Processa a mensagem, prediz o sentimento e atualiza o banco de dados.

    Args:
        message: A mensagem do RabbitMQ contendo os dados da avaliação.

    Raises:
        Exception: Se ocorrer algum erro durante o processamento.
    """
    try:
        message_data = json.loads(message.body.decode("utf-8"))

        print("message_data", message_data)

        review_id = message_data["review_id"]
        review_bytes = message_data["review_bytes"]
        review_sentence = base64.b64decode(review_bytes).decode("utf-8")

        print("review", review_sentence)

        today = datetime.today().strftime("%Y-%m-%d")

        prediction = analyzer.predict(review_sentence)

        with review_repository.sessionmaker() as session:
            review = review_repository.update_review(session, review_id)

            if review:
                review.classification = prediction.output
                review.pos_score = round(prediction.probas["POS"], 3)
                review.neg_score = round(prediction.probas["NEG"], 3)
                review.neu_score = round(prediction.probas["NEU"], 3)
                review.classified_at = today
                review.classified = True

                session.commit()

            else:
                logger.warning(f"Review with id {review_id} not found")

        logger.info(f"Prediction for id {review_id} completed successfully.")

    except Exception as exc:
        logger.error(f"Prediction failed: {exc}")

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
