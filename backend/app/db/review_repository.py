from typing import List
import asyncpg


from app.models.review import CreateReviewModel
from app.utils import get_logger
from app.utils.decorators import monitor_db_operation

logger = get_logger(__name__)


class ReviewRepository:
    @monitor_db_operation("get_reviews")
    async def get_reviews(self, session, *args) -> List[asyncpg.Record]:
        query = "SELECT * from reviews_partitioned"
        row = await session.fetch(query, *args)
        return row

    @monitor_db_operation("get_review_by_id")
    async def get_review_by_id(
        self, session: asyncpg.Connection, review_id: str
    ) -> asyncpg.Record | None:
        query = "SELECT * FROM reviews_partitioned WHERE id = $1"
        return await session.fetchrow(query, review_id)

    @monitor_db_operation("create_review")
    async def create_review(
        self, session: asyncpg.Connection, review: CreateReviewModel
    ) -> asyncpg.Record | None:
        query = """
        INSERT INTO reviews_partitioned (
           company_id, customer_id, review_date, review_data
        ) VALUES ($1, $2, $3, $4)
        RETURNING *;
        """
        return await session.fetchrow(
            query,
            review.company_id,
            review.customer_id,
            review.review_date,
            review.review_data,
        )

    @monitor_db_operation("get_classification_count")
    async def get_classification_count(self, session, start_date, end_date):
        query = """
            SELECT classification, COUNT(*) FROM reviews_partitioned 
            WHERE classified_at IS NOT NULL
            AND review_date BETWEEN $1 AND $2 
            GROUP BY classification;
        """

        return await session.fetch(query, start_date, end_date)

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
