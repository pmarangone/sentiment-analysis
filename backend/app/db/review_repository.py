from typing import List
import asyncpg


from app.db.schemas.review import ReviewSchema
from app.models.review import CreateReviewModel
from app.utils import get_logger
from app.utils.decorators import monitor_db_operation

logger = get_logger(__name__)


class ReviewRepository:
    @monitor_db_operation("get_reviews")
    async def get_reviews(self, session, *args) -> List:
        return session.query(ReviewSchema).all()

    @monitor_db_operation("get_review_by_id")
    async def get_review_by_id(
        self, session, review_id: str
    ) -> ReviewSchema | None:
        return session.query(ReviewSchema).filter(ReviewSchema.id == review_id).first()

    @monitor_db_operation("create_review")
    async def create_review(
        self, session, review: CreateReviewModel
    ) -> ReviewSchema | None:
        new_review = ReviewSchema(
           company_id=str(review.company_id),
           customer_id=str(review.customer_id),
           review_date=review.review_date,
           review_data=review.review_data,
        )
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
        return new_review

    @monitor_db_operation("get_classification_count")
    async def get_classification_count(self, session, start_date, end_date):
        from sqlalchemy import func
        return session.query(
            ReviewSchema.classification, func.count(ReviewSchema.id)
        ).filter(
            ReviewSchema.classified_at != None,
            ReviewSchema.review_date.between(start_date, end_date)
        ).group_by(ReviewSchema.classification).all()

    @monitor_db_operation("create_reviews_many")
    async def create_reviews_many(self, session, reviews):
        values_placeholders = ", ".join(
            f"(${i * 4 + 1}, ${i * 4 + 2}, ${i * 4 + 3}, ${i * 4 + 4})"
            for i in range(len(reviews))
        )
        query = """
            INSERT INTO reviews_partitioned (company_id, customer_id, review_date, review_data)
            VALUES {}
            RETURNING id, review_data;
        """.format(values_placeholders)

        flattened_values = []
        for review in reviews:
            flattened_values.extend(
                [
                    review.company_id,
                    review.customer_id,
                    review.review_date,
                    review.review_data,
                ]
            )

        return await session.fetch(query, *flattened_values)
