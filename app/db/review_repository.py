from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from app.db.schemas import Base
from app.db.schemas.review import ReviewSchema
from app.models.review import BaseReviewModel, ReviewModel
from app.utils import get_logger

logger = get_logger(__name__)


class ReviewRepository:
    def __init__(self, url):
        logger.info("Creating database connection")

        # TODO: handle the database connection properly
        # do not initialize it if create_engine fails
        self.engine = create_engine(url)
        self.sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def initialize_schema(self):
        logger.info("Creating database schemas")
        Base.metadata.create_all(bind=self.engine)

    def get_reviews(self, session):
        return session.query(ReviewSchema).all()

    def get_review_by_id(self, session, review_id: str) -> ReviewSchema:
        return session.query(ReviewSchema).filter_by(id=review_id).first()

    def create_review(self, session, review: BaseReviewModel) -> ReviewSchema:
        new_review = ReviewSchema(**review.model_dump())
        session.add(new_review)
        return new_review
