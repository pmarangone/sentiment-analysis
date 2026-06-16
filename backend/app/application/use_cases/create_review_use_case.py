from app.domain.repositories.review_repository_interface import ReviewRepositoryInterface
from app.models.review import RequestReviewModel, CreateReviewModel
from app.db.schemas.review import ReviewSchema
import base64
import json

class CreateReviewUseCase:
    def __init__(self, review_repository: ReviewRepositoryInterface, celery_app):
        self.review_repository = review_repository
        self.celery_app = celery_app

    async def execute(self, db_session, review_data: RequestReviewModel, customer_id: str):
        review = CreateReviewModel(
            company_id=review_data.company_id,
            customer_id=customer_id,
            review_date=review_data.review_date,
            review_data=review_data.review_data,
        )
        row = await self.review_repository.create_review(db_session, review)
        created_review = ReviewSchema(**dict(row))

        message = {
            "review_id": str(created_review.id),
            "review_bytes": base64.b64encode(
                created_review.review_data.encode()
            ).decode("utf-8"),
        }

        json_data = json.dumps(message)

        self.celery_app.send_task(
            "sentiment-analysis-consumer", args=[json_data], queue="sentiment-analysis"
        )
        return created_review
