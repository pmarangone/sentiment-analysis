import uuid
from pydantic import BaseModel, Field


class BaseReviewModel(BaseModel):
    customer_name: str = Field(...)
    review_date: str = Field(...)
    review_data: str = Field(...)


class ReviewModel(BaseReviewModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    classification: str = Field(...)
