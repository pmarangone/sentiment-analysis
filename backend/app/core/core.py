import base64
import json
import uuid
from sqlalchemy.orm import Session

from app import celery_app
from app.api.responses import created, not_found, server_error, success
from app.db import ReviewRepository, CustomerRepository

from app.models.review import CreateReviewModel, RequestReviewModel
from app.utils.logger import get_logger
from app.db.schemas.review import ReviewSchema
from app.db.schemas.customer import Customer

review_repository = ReviewRepository()
customer_repository = CustomerRepository()

logger = get_logger(__name__)


async def check_customer_exists(db_session, customer_name):
    row = await customer_repository.get_customer_by_name(db_session, customer_name)
    if not row:
        row = await customer_repository.create_customer(db_session, customer_name)

        if not row:
            raise Exception("Customer was not")

    return Customer(**dict(row))


async def core_create_reviews_many(
    db_session: Session,
    reviews: RequestReviewModel,
):
    try:
        result = await customer_repository.insert_many(
            db_session, [review["customer_name"] for review in reviews.reviews]
        )

        customer_map = {row["name"]: row["id"] for row in result}

        reviews = [
            CreateReviewModel(
                company_id=reviews.company_id,
                customer_id=customer_map[review["customer_name"]],
                review_date=review["review_date"],
                review_data=review["review_data"],
            )
            for review in reviews.reviews
        ]

        rows = await review_repository.create_reviews_many(db_session, reviews)
        created_reviews = [ReviewSchema(**dict(row)) for row in rows]

        logger.info(f"Created {len(created_reviews)} reviews")

        message = [
            {
                "review_id": str(created.id),
                "review_bytes": base64.b64encode(created.review_data.encode()).decode(
                    "utf-8"
                ),
            }
            for created in created_reviews
        ]

        json_data = json.dumps(message)

        _task = celery_app.send_task(
            "sentiment-analysis-consumer-many",
            args=[json_data],
            queue="sentiment-analysis",
        )

        return created(created_reviews)

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while creating review: {error}")
        return server_error(error)


async def core_create_review_celery(
    db_session: Session,
    review: RequestReviewModel,
):
    """Cria a avaliação no banco de dados e envia a avaliação e o ID da entrada
    no banco de dados para o consumidor.

    Args:
    request: Instância de fastapi.Request
    review: Instância derivada de pydantic.BaseModel, que foi enviado no corpo da requisição.

    Returns:
    criada: A entrada do usuário tal como foi criada no banco de dados.
    erro_servidor: Mensagem de erro, seja em criar a entrada no banco de dados ou em enviar a mensagem para
    o consumidor.
    """
    try:
        customer = check_customer_exists(db_session, review.customer_name)

        review = CreateReviewModel(
            company_id=review.company_id,
            customer_id=customer.id,
            review_date=review.review_date,
            review_data=review.review_data,
        )
        row = await review_repository.create_review(db_session, review)
        created_review = ReviewSchema(**dict(row))

        logger.info(f"Created review: {created_review}")

        message = {
            "review_id": str(created_review.id),
            "review_bytes": base64.b64encode(
                created_review.review_data.encode()
            ).decode("utf-8"),
        }

        json_data = json.dumps(message)

        _task = celery_app.send_task(
            "sentiment-analysis-consumer", args=[json_data], queue="sentiment-analysis"
        )
        return created(created_review)

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while creating review: {error}")
        return server_error(error)


async def core_get_review_by_id(db_session: Session, id: uuid.UUID):
    """Busca no banco de dados uma avaliação pelo id.

    Args:
    request: Instância de fastapi.Request
    id: Instância uuid.UUID referente a avaliação

    Returns:
    sucesso: A avaliação do usuário
    não_encontrado: Retorno padrão caso nenhum entrada com o id seja encontrada no banco de dados
    erro_servidor: Mensagem de erro
    """
    try:
        review = await review_repository.get_review_by_id(db_session, id)

        if review:
            return success(review)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching review with id {id}: {error}")
        return server_error(error)


async def core_get_reviews(
    db_session: Session,
):
    """Busca no banco de dados todas as avaliações.

    Args:
    request: Instância de fastapi.Request

    Returns:
    sucesso: Lista, do tipo Json, com todas as avaliações
    não_encontrado: Retorno padrão caso nenhuma entrada seja encontrada no banco de dados
    erro_servidor: Mensagem de erro
    """
    try:
        reviews = await review_repository.get_reviews(db_session)

        if reviews:
            return success(reviews)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching reviews: {error}")
        return server_error(error)


def core_generate_report(data):
    classification_mapping = {"POS": 0, "NEG": 0, "NEU": 0}
    for classification, count in data:
        classification_mapping[classification] = count

    return {
        "positiva": classification_mapping["POS"],
        "negativa": classification_mapping["NEG"],
        "neutra": classification_mapping["NEU"],
    }


async def core_get_classification_count(db_session: Session, start_date, end_date):
    """Gera um relatório do número de avaliações positivas, negativas ou neutras
    feitas entre a data inicial e a data final (inclusiva).

    Args:
    request: Instância de fastapi.Request
    start_date: A data inicial da busca
    end_date: A data final da busca

    Returns:
    sucesso: Lista, do tipo Json, com todas as avaliações feitas entre a data inicial e data final
    não_encontrado: Retorno padrão caso nenhuma entrada seja encontrada no banco de dados
    erro_servidor: Mensagem de erro
    """
    try:
        result = await review_repository.get_classification_count(
            db_session, start_date.date(), end_date.date()
        )

        if result:
            report = core_generate_report(result)
            return success(report)

        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching report: {error}")
        return server_error(error)
