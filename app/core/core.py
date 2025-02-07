import uuid
from fastapi import Request
from app.api.responses import created, not_found, server_error, success
from app.db.review_repository import ReviewRepository
from app.models.review import BaseReviewModel
from app.utils.logger import get_logger

logger = get_logger(__name__)


def core_create_review(request: Request, review: BaseReviewModel):
    repository: ReviewRepository = request.app.state.review_repository

    try:
        with repository.sessionmaker() as session:
            created_review = repository.create_review(session, review)
            session.commit()

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
