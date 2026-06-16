from app.domain.interfaces import IReviewRepository
from app.domain.models import Review
from typing import List

class GetAllReviewsUseCase:
    def __init__(self, review_repo: IReviewRepository):
        self.review_repo = review_repo

    async def execute(self) -> List[Review]:
        return await self.review_repo.get_all()
