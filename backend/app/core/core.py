import base64
import json
import uuid
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app import celery_app
from app.api.responses import OK, created, not_found, server_error, success
from app.db import ReviewRepository, CustomerRepository

from app.models.review import CreateReviewModel, RequestReviewModel
from app.utils.logger import get_logger
from app.config import DATABASE_URL

review_repository = ReviewRepository(DATABASE_URL)
customer_repository = CustomerRepository(DATABASE_URL)

logger = get_logger(__name__)


async def core_create_review(
    request: Request,
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
        created_review = review_repository.create_review(db_session, review)
        db_session.commit()
        db_session.refresh(created_review)

        message = {
            "review_id": str(created_review.id),
            "review_bytes": base64.b64encode(
                created_review.review_data.encode()
            ).decode("utf-8"),
        }

        # await rabbitmq_pool.publish_message(json.dumps(message))

        return created(created_review)

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while creating review: {error}")
        return server_error(error)


async def core_create_review_celery(
    request: Request,
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
        customer = customer_repository.get_customer_by_name(
            db_session, review.customer_name
        )
        if not customer:
            customer = customer_repository.create_customer(
                db_session, review.customer_name
            )
            db_session.commit()
            db_session.refresh(customer)

        review = CreateReviewModel(
            customer_id=customer.id,
            review_date=review.review_date,
            review_data=review.review_data,
        )
        created_review = review_repository.create_review(db_session, review)
        db_session.commit()
        db_session.refresh(created_review)

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


def core_get_review_by_id(request: Request, db_session: Session, id: uuid.UUID):
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
        review = review_repository.get_review_by_id(db_session, id)

        if review:
            return success(review)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching review with id {id}: {error}")
        return server_error(error)


def core_get_reviews(
    request: Request,
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
        reviews = review_repository.get_reviews(db_session)

        if reviews:
            return success(reviews)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching reviews: {error}")
        return server_error(error)


def core_get_classification_count(
    request: Request, db_session: Session, start_date, end_date
):
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
        result = review_repository.get_classification_count(
            db_session, start_date, end_date
        )

        print(result)

        classification_mapping = {"positive": 0, "negative": 0, "neutral": 0}
        for classification, count in result:
            classification_mapping[classification] = count

        report = {
            "positiva": classification_mapping["positive"],
            "negativa": classification_mapping["negative"],
            "neutra": classification_mapping["neutral"],
        }

        if report:
            return success(report)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching report: {error}")
        return server_error(error)
