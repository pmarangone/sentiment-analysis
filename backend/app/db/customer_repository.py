from typing import List

import asyncpg
from app.utils import get_logger

logger = get_logger(__name__)


class CustomerRepository:
    # TODO
    # def initialize_schema(self, engine):
    #     logger.info("Creating database schemas")
    #     Base.metadata.create_all(bind=engine)

    async def get_customers(self, session) -> List[asyncpg.Record]:
        query = "SELECT * FROM customers"
        return await session.fetch(query)

    async def get_customer_by_name(
        self, session, customer_name: str
    ) -> asyncpg.Record | None:
        query = "SELECT * FROM customers WHERE name = $1"
        return await session.fetchrow(query, customer_name)

    async def create_customer(
        self, session, customer_name: str
    ) -> asyncpg.Record | None:
        query = "INSERT INTO customers (name) VALUES ($1) RETURNING *"
        return await session.fetchrow(query, customer_name)
