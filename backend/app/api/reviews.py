from datetime import datetime
from typing import Annotated
import uuid
from fastapi import (
    APIRouter,
    Query,
    Request,
)

from app.api.responses import created, not_found, server_error, success
from app.core.core import (
    core_create_review_celery,
    core_create_reviews_many,
    core_get_review_by_id,
    core_get_reviews,
    core_get_classification_count,
)
from app.models.review import RequestReviewModel, RequestReviewsManyModel
from app.utils.logger import get_logger

from app.db.session import PostgresDep


logger = get_logger(__name__)
reviews_router = APIRouter(prefix="/reviews")


@reviews_router.get("/")
async def get_reviews(request: Request, db_session: PostgresDep):
    try:
        reviews = await core_get_reviews(db_session)
        if reviews:
            return success(reviews)
        return not_found()
    except Exception as exc:
        logger.error(f"Error while fetching reviews: {str(exc)}")
        return server_error(str(exc))


@reviews_router.post("/celery")
async def post_review_celery(
    request: Request,
    review: RequestReviewModel,
    db_session: PostgresDep,
):
    try:
        created_review = await core_create_review_celery(db_session, review)
        return created(created_review)
    except Exception as exc:
        logger.error(f"Error while creating review: {str(exc)}")
        return server_error(str(exc))


@reviews_router.post("/many")
async def post_reviews_many(
    request: Request,
    reviews: RequestReviewsManyModel,
    db_session: PostgresDep,
):
    try:
        created_reviews = await core_create_reviews_many(db_session, reviews)
        return created(created_reviews)
    except Exception as exc:
        logger.error(f"Error while creating reviews: {str(exc)}")
        return server_error(str(exc))


@reviews_router.get("/report")
async def get_reviews_report(
    request: Request,
    start_date: Annotated[datetime, Query()],
    end_date: Annotated[datetime, Query()],
    db_session: PostgresDep,
):
    try:
        report = await core_get_classification_count(db_session, start_date, end_date)
        if report:
            return success(report)
        return not_found()
    except Exception as exc:
        logger.error(f"Error while fetching report: {str(exc)}")
        return server_error(str(exc))


@reviews_router.get("/{id}")
async def get_review_by_id(request: Request, id: uuid.UUID, db_session: PostgresDep):
    try:
        review = await core_get_review_by_id(db_session, id)
        if review:
            return success(review)
        return not_found()
    except Exception as exc:
        logger.error(f"Error while fetching review with id {id}: {str(exc)}")
        return server_error(str(exc))
