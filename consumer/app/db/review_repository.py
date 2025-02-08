from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.db.schemas import Base
from app.db.schemas.review import ReviewSchema
from app.utils.logger import get_logger

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

    def update_review(self, session, review_id: str, classification):
        review: ReviewSchema = (
            session.query(ReviewSchema)
            .with_for_update()
            .filter_by(id=review_id)
            .first()
        )

        review.classification = classification
        review.classified = True


review_repository = ReviewRepository(DATABASE_URL)
