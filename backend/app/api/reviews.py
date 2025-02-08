from typing import Annotated
import uuid
from fastapi import (
    APIRouter,
    Query,
    Request,
)

from app.core.core import core_create_review, core_get_review_by_id, core_get_reviews
from app.models.review import BaseReviewModel
from app.utils.logger import get_logger


logger = get_logger(__name__)
reviews_router = APIRouter(prefix="/reviews")


@reviews_router.get("/")
async def get_reviews(request: Request):
    return core_get_reviews(request)


@reviews_router.post("/")
async def post_review(request: Request, review: BaseReviewModel):
    return await core_create_review(request, review)


@reviews_router.get("/report")
async def get_reviews_report(
    start_date: Annotated[str, Query()],
    end_date: Annotated[str, Query()],
):
    print(start_date, end_date)
    pass


@reviews_router.get("/{id}")
async def get_review_by_id(request: Request, id: uuid.UUID):
    return core_get_review_by_id(request, id)
