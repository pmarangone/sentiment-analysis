import base64
import json
import uuid
from fastapi import Request
from app.api.responses import created, not_found, server_error, success
from app.db.review_repository import ReviewRepository
from app.models.review import BaseReviewModel
from app.utils.logger import get_logger

from .publisher import RabbitMQPool

logger = get_logger(__name__)


async def core_create_review(request: Request, review: BaseReviewModel):
    repository: ReviewRepository = request.app.state.review_repository
    rabbitmq_pool: RabbitMQPool = request.app.state.rabbitmq_pool

    try:
        with repository.sessionmaker() as session:
            created_review = repository.create_review(session, review)
            session.commit()
            session.refresh(created_review)

        message = {
            "review_id": str(created_review.id),
            "review_bytes": base64.b64encode(
                created_review.review_data.encode()
            ).decode("utf-8"),
        }

        await rabbitmq_pool.publish_message(json.dumps(message))

        return created(created_review)

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while creating review: {error}")
        return server_error(error)


def core_get_review_by_id(request: Request, id: uuid.UUID):
    repository: ReviewRepository = request.app.state.review_repository

    try:
        with repository.sessionmaker() as session:
            review = repository.get_review_by_id(session, id)

        if review:
            return success(review)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching review with id {id}: {error}")
        return server_error(error)


def core_get_reviews(request: Request):
    repository: ReviewRepository = request.app.state.review_repository

    try:
        with repository.sessionmaker() as session:
            reviews = repository.get_reviews(session)

        if reviews:
            return success(reviews)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching reviews: {error}")
        return server_error(error)


def core_get_classification_count(request: Request, start_date, end_date):
    repository: ReviewRepository = request.app.state.review_repository

    try:
        with repository.sessionmaker() as session:
            report = repository.get_classification_count(session, start_date, end_date)

        if report:
            return success(report)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching report: {error}")
        return server_error(error)
