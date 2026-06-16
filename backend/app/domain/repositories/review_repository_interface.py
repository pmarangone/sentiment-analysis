from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

class ReviewRepositoryInterface(ABC):
    @abstractmethod
    async def get_reviews(self, *args) -> List:
        pass

    @abstractmethod
    async def get_review_by_id(self, review_id: uuid.UUID) -> Optional[dict]:
        pass

    @abstractmethod
    async def create_review(self, review: dict) -> dict:
        pass

    @abstractmethod
    async def get_classification_count(self, start_date, end_date) -> List:
        pass

    @abstractmethod
    async def create_reviews_many(self, reviews: List) -> List:
        pass
