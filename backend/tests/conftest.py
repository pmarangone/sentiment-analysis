from datetime import date
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.schemas import Base
from app.db.review_repository import ReviewRepository
from app.models.review import BaseReviewModel
from app.db.schemas.review import ReviewSchema

DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def db_session():
    """Cria uma banco de dados e uma sessão para cada teste"""
    engine = create_engine(DATABASE_URL)
    _sessionmaker = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    session = _sessionmaker()
    yield session

    session.close()


@pytest.fixture
def repository():
    """Cria o repositório responsável pelas operações no banco de dados"""
    return ReviewRepository(DATABASE_URL)


@pytest.fixture
def review_model():
    """Fixture do modelo de uma avaliação"""
    base_review = BaseReviewModel(
        customer_name="Patrick",
        review_date=date(2025, 1, 1),
        review_data="Maravilhoso!",
    )
    return base_review


@pytest.fixture
def review_schema():
    """Fixture da schema de uma avaliação"""

    def _create_review(
        customer_name="Patrick", classification="POS", review_date=date(2025, 1, 1)
    ):
        return ReviewSchema(
            customer_name=customer_name,
            review_date=review_date,
            review_data="Eu tenho tantas críticas para fazer... a mim mesmo por não ter descoberto isso antes!",
            classification=classification,
            classified=True,
            classified_at=date(2025, 1, 2),
            pos_score=0.98,
            neg_score=0.01,
            neu_score=0.01,
        )

    return _create_review
