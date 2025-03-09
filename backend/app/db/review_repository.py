from typing import List
import asyncpg
from sqlalchemy import text

from app.db.schemas import Base
from app.db.schemas.review import ReviewSchema

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
        query = "SELECT * from reviews"
        row = await session.fetch(query, *args)
        return row

    async def get_review_by_id(
        self, session: asyncpg.Connection, review_id: str
    ) -> asyncpg.Record | None:
        query = "SELECT * FROM reviews WHERE id = $1"
        return await session.fetchrow(query, review_id)

    async def create_review(
        self, session: asyncpg.Connection, review: CreateReviewModel
    ) -> asyncpg.Record | None:
        query = """
        INSERT INTO reviews (
           customer_id, review_date, review_data
        ) VALUES ($1, $2, $3)
        RETURNING *;
        """
        return await session.fetchrow(
            query, review.customer_id, review.review_date, review.review_data
        )

    async def get_classification_count(self, session, start_date, end_date):
        query = """
            SELECT classification, COUNT(*) FROM reviews 
            WHERE classified_at IS NOT NULL
            AND review_date BETWEEN $1 AND $2 
            GROUP BY classification;
        """

        return await session.fetch(query, start_date, end_date)
