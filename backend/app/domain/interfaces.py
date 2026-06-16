from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models import Review, Customer
import uuid

class IReviewRepository(ABC):
    @abstractmethod
    async def create(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def get_by_id(self, review_id: uuid.UUID) -> Optional[Review]:
        pass

    @abstractmethod
    async def get_all(self) -> list[Review]:
        pass

class ICustomerRepository(ABC):
    @abstractmethod
    async def get_by_id(self, customer_id: uuid.UUID) -> Optional[Customer]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Customer]:
        pass

    @abstractmethod
    async def create(self, customer: Customer) -> Customer:
        pass

class IMessageBroker(ABC):
    @abstractmethod
    async def publish(self, topic: str, message: dict):
        pass
