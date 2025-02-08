import uuid
from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.schemas import Base


class ReviewSchema(Base):
    __tablename__ = "reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    customer_name = Column(String, nullable=False)
    review_date = Column(String, nullable=False)
    review_data = Column(String, nullable=False)
    # Updated asynchronously
    classification = Column(String, default="")
    # Retries
    classified = Column(Boolean, default=False, nullable=False, index=True)
