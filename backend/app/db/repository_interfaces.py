from abc import ABC, abstractmethod
from typing import List, Any
import asyncpg


class ICustomerRepository(ABC):
    @abstractmethod
    async def get_customers(self, session: asyncpg.Connection) -> List[asyncpg.Record]:
        pass

    @abstractmethod
    async def get_customer_by_name(
        self, session: asyncpg.Connection, customer_name: str
    ) -> asyncpg.Record | None:
        pass

    @abstractmethod
    async def create_customer(
        self, session: asyncpg.Connection, customer_name: str
    ) -> asyncpg.Record | None:
        pass

    @abstractmethod
    async def insert_many(
        self, session: asyncpg.Connection, customers: List[str]
    ) -> List[asyncpg.Record]:
        pass


class IReviewRepository(ABC):
    @abstractmethod
    async def get_reviews(self, session: asyncpg.Connection, *args: Any) -> List[asyncpg.Record]:
        pass

    @abstractmethod
    async def get_review_by_id(
        self, session: asyncpg.Connection, review_id: str
    ) -> asyncpg.Record | None:
        pass

    @abstractmethod
    async def create_review(
        self, session: asyncpg.Connection, review: Any
    ) -> asyncpg.Record | None:
        pass

    @abstractmethod
    async def get_classification_count(
        self, session: asyncpg.Connection, start_date: Any, end_date: Any
    ) -> List[asyncpg.Record]:
        pass

    @abstractmethod
    async def create_reviews_many(
        self, session: asyncpg.Connection, reviews: List[Any]
    ) -> List[asyncpg.Record]:
        pass
