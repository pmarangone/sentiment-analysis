from app.domain.interfaces import IReviewRepository
from app.domain.models import Review
import uuid
from typing import Optional

class GetReviewUseCase:
    def __init__(self, review_repo: IReviewRepository):
        self.review_repo = review_repo

    async def execute(self, review_id: uuid.UUID) -> Optional[Review]:
        return await self.review_repo.get_by_id(review_id)
