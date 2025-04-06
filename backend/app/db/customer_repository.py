from typing import List

import asyncpg
from app.utils import get_logger
from app.utils.decorators import monitor_db_operation

logger = get_logger(__name__)


class CustomerRepository:
    @monitor_db_operation("get_customers")
    async def get_customers(self, session) -> List[asyncpg.Record]:
        query = "SELECT * FROM customers"
        return await session.fetch(query)

    @monitor_db_operation("get_customer_by_name")
    async def get_customer_by_name(
        self, session, customer_name: str
    ) -> asyncpg.Record | None:
        query = "SELECT * FROM customers WHERE name = $1"
        return await session.fetchrow(query, customer_name)

    @monitor_db_operation("create_customer")
    async def create_customer(
        self, session, customer_name: str
    ) -> asyncpg.Record | None:
        query = "INSERT INTO customers (name) VALUES ($1) RETURNING *"
        return await session.fetchrow(query, customer_name)

    @monitor_db_operation("create_customer_many")
    async def insert_many(self, session, customers):
        values_placeholders = ", ".join(f"(${i + 1})" for i in range(len(customers)))
        query = """
            WITH ins AS (
                INSERT INTO customers (name)
                VALUES {}
                ON CONFLICT (name) DO NOTHING
                RETURNING id, name
            )
            SELECT id, name FROM ins
            UNION ALL
            SELECT id, name FROM customers WHERE name = ANY(${})
        """.format(values_placeholders, len(customers) + 1)

        return await session.fetch(query, *customers, customers)
