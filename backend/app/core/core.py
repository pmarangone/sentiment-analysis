import base64
import json
import uuid
from sqlalchemy.orm import Session

from app import celery_app
from app.db import ReviewRepository, CustomerRepository

from app.models.review import CreateReviewModel, RequestReviewModel
from app.utils.logger import get_logger
from app.db.schemas.review import ReviewSchema
from app.db.schemas.customer import Customer

review_repository = ReviewRepository()
customer_repository = CustomerRepository()

logger = get_logger(__name__)


async def check_customer_exists(db_session, customer_name):
    row = await customer_repository.get_customer_by_name(db_session, customer_name)
    if not row:
        row = await customer_repository.create_customer(db_session, customer_name)

        if not row:
            raise Exception("Customer was not")

    return Customer(**dict(row))


async def core_create_reviews_many(
    db_session: Session,
    reviews: RequestReviewModel,
):
    result = await customer_repository.insert_many(
        db_session, [review["customer_name"] for review in reviews.reviews]
    )

    customer_map = {row["name"]: row["id"] for row in result}

    reviews_list = [
        CreateReviewModel(
            company_id=reviews.company_id,
            customer_id=customer_map[review["customer_name"]],
            review_date=review["review_date"],
            review_data=review["review_data"],
        )
        for review in reviews.reviews
    ]

    rows = await review_repository.create_reviews_many(db_session, reviews_list)
    created_reviews = [ReviewSchema(**dict(row)) for row in rows]

    logger.info(f"Created {len(created_reviews)} reviews")

    message = [
        {
            "review_id": str(created.id),
            "review_bytes": base64.b64encode(created.review_data.encode()).decode(
                "utf-8"
            ),
        }
        for created in created_reviews
    ]

    json_data = json.dumps(message)

    celery_app.send_task(
        "sentiment-analysis-consumer-many",
        args=[json_data],
        queue="sentiment-analysis",
    )

    return created_reviews


async def core_create_review_celery(
    db_session: Session,
    review: RequestReviewModel,
):
    customer = await check_customer_exists(db_session, review.customer_name)

    review_model = CreateReviewModel(
        company_id=review.company_id,
        customer_id=customer.id,
        review_date=review.review_date,
        review_data=review.review_data,
    )
    row = await review_repository.create_review(db_session, review_model)
    created_review = ReviewSchema(**dict(row))

    logger.info(f"Created review: {created_review}")

    message = {
        "review_id": str(created_review.id),
        "review_bytes": base64.b64encode(
            created_review.review_data.encode()
        ).decode("utf-8"),
    }

    json_data = json.dumps(message)

    celery_app.send_task(
        "sentiment-analysis-consumer", args=[json_data], queue="sentiment-analysis"
    )
    return created_review


async def core_get_review_by_id(db_session: Session, id: uuid.UUID):
    review = await review_repository.get_review_by_id(db_session, id)
    return review


async def core_get_reviews(
    db_session: Session,
):
    reviews = await review_repository.get_reviews(db_session)
    return reviews


def core_generate_report(data):
    classification_mapping = {"POS": 0, "NEG": 0, "NEU": 0}
    for classification, count in data:
        classification_mapping[classification] = count

    return {
        "positiva": classification_mapping["POS"],
        "negativa": classification_mapping["NEG"],
        "neutra": classification_mapping["NEU"],
    }


async def core_get_classification_count(db_session: Session, start_date, end_date):
    result = await review_repository.get_classification_count(
        db_session, start_date.date(), end_date.date()
    )

    if not result:
        return None

    return core_generate_report(result)
