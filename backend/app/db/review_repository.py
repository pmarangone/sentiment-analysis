from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import sessionmaker

from app.db.schemas import Base
from app.db.schemas.review import ReviewSchema
from app.models.review import BaseReviewModel, ReviewModel
from app.utils import get_logger

logger = get_logger(__name__)


class ReviewRepository:
    def __init__(self, url):
        logger.info("Creating database connection")

        try:
            # TODO: handle the database connection properly
            # do not initialize it if create_engine fails
            self.engine = create_engine(url)
            self.sessionmaker = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )

        except Exception as exc:
            error = str(exc)
            logger.error(f"Error occurred: {error}")
            raise error

    def initialize_schema(self):
        logger.info("Creating database schemas")
        Base.metadata.create_all(bind=self.engine)

    def get_reviews(self, session):
        return session.query(ReviewSchema).all()

    def get_review_by_id(self, session, review_id: str) -> ReviewSchema:
        return session.query(ReviewSchema).filter_by(id=review_id).first()

    def get_classification_count(self, session, start_date, end_date):
        query = text("""
        SELECT classification, COUNT(*) FROM reviews 
        WHERE classified = true
        AND review_date BETWEEN :start_date AND :end_date 
        GROUP BY classification;
        """)

        result = session.execute(
            query, {"start_date": start_date, "end_date": end_date}
        ).fetchall()

        classification_mapping = {"POS": 0, "NEG": 0, "NEU": 0}
        for classification, count in result:
            classification_mapping[classification] = count

        report = {
            "positiva": classification_mapping["POS"],
            "negativa": classification_mapping["NEG"],
            "neutra": classification_mapping["NEU"],
        }

        return report

    def create_review(self, session, review: BaseReviewModel) -> ReviewSchema:
        new_review = ReviewSchema(**review.model_dump())
        session.add(new_review)
        return new_review
