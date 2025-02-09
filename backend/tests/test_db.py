from datetime import date
import pytest

from app.db.schemas.review import ReviewSchema


def test_initialize_schema(repository):
    """Testa a inicialização das schemas"""
    try:
        repository.initialize_schema()
    except Exception as exc:
        pytest.fail(f"Inicialização das schemas falhou: {exc}")


def test_create_review(repository, db_session, review_model):
    """Testa criar uma avaliação"""
    new_review = review_model

    created_review = repository.create_review(db_session, new_review)
    db_session.commit()

    fetched_review = (
        db_session.query(ReviewSchema).filter_by(id=created_review.id).first()
    )

    assert fetched_review is not None
    assert fetched_review.customer_name == new_review.customer_name


def test_get_reviews(repository, db_session, review_schema):
    """Testa a busca de todas as avaliações"""
    date1 = date(2025, 1, 1)
    date2 = date(2025, 1, 2)

    review1 = review_schema(review_date=date1)
    review2 = review_schema(review_date=date2)

    db_session.add_all([review1, review2])
    db_session.commit()

    reviews = repository.get_reviews(db_session)

    assert len(reviews) == 2
    assert reviews[0].review_date == date1
    assert reviews[1].review_date == date2


def test_get_review_by_id(repository, db_session, review_schema):
    """Testa a busca por id"""
    customer_name = "Patrick"
    review = review_schema(customer_name=customer_name)

    db_session.add(review)
    db_session.commit()

    fetched_review = repository.get_review_by_id(db_session, review.id)

    assert fetched_review is not None
    assert fetched_review.customer_name == customer_name


def test_get_classification_count(repository, db_session, review_schema):
    """Testa a contagem de classificação de avaliações"""
    test_date = date(2025, 1, 1)
    review1 = review_schema(classification="POS", review_date=test_date)
    review2 = review_schema(classification="NEG", review_date=test_date)
    review3 = review_schema(classification="NEU", review_date=test_date)

    db_session.add_all([review1, review2, review3])
    db_session.commit()

    result = repository.get_classification_count(
        db_session, test_date, date(2025, 1, 2)
    )

    report = {row[0]: row[1] for row in result}

    assert report["POS"] == 1
    assert report["NEG"] == 1
    assert report["NEU"] == 1
