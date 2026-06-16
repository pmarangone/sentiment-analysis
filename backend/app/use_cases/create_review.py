import base64
import json
from app.domain.models import Review, Customer
from app.domain.interfaces import IReviewRepository, ICustomerRepository, IMessageBroker
import uuid
from datetime import date

class CreateReviewUseCase:
    def __init__(self, review_repo: IReviewRepository, customer_repo: ICustomerRepository, broker: IMessageBroker):
        self.review_repo = review_repo
        self.customer_repo = customer_repo
        self.broker = broker

    async def execute(self, company_id: uuid.UUID, customer_name: str, review_date: date, review_data: str) -> Review:
        customer = await self.customer_repo.get_by_name(customer_name)
        if not customer:
            customer = await self.customer_repo.create(Customer(name=customer_name))
        
        review = Review(
            customer_id=customer.id,
            company_id=company_id,
            review_date=review_date,
            review_data=review_data,
        )
        saved_review = await self.review_repo.create(review)
        
        # Publish to broker
        message = {
            "review_id": str(saved_review.id),
            "review_bytes": base64.b64encode(
                saved_review.review_data.encode()
            ).decode("utf-8"),
        }
        await self.broker.publish("sentiment-analysis", json.dumps(message))
        
        return saved_review
