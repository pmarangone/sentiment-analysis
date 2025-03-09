from typing import List
import asyncpg


from app.models.review import CreateReviewModel
from app.utils import get_logger

logger = get_logger(__name__)


class ReviewRepository:
    # TODO
    # def initialize_schema(self, engine):
    #     """Inicializa as tabelas no banco de dados."""
    #     logger.info("Creating database schemas")
    #     Base.metadata.create_all(bind=engine)

    async def get_reviews(self, session, *args) -> List[asyncpg.Record]:
        query = "SELECT * from reviews_partitioned"
        row = await session.fetch(query, *args)
        return row

    async def get_review_by_id(
        self, session: asyncpg.Connection, review_id: str
    ) -> asyncpg.Record | None:
        query = "SELECT * FROM reviews_partitioned WHERE id = $1"
        return await session.fetchrow(query, review_id)

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

    async def get_classification_count(self, session, start_date, end_date):
        query = """
            SELECT classification, COUNT(*) FROM reviews_partitioned 
            WHERE classified_at IS NOT NULL
            AND review_date BETWEEN $1 AND $2 
            GROUP BY classification;
        """

        return await session.fetch(query, start_date, end_date)
