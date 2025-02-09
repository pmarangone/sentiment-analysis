import base64
import json
import uuid
from fastapi import Request
from app.api.responses import OK, created, not_found, server_error, success
from app.db.review_repository import ReviewRepository
from app.models.review import BaseReviewModel
from app.utils.logger import get_logger

from .publisher import RabbitMQPool

logger = get_logger(__name__)


async def core_create_review(request: Request, review: BaseReviewModel):
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
        repository: ReviewRepository = request.app.state.review_repository
        rabbitmq_pool: RabbitMQPool = request.app.state.rabbitmq_pool

        with repository.sessionmaker() as session:
            created_review = repository.create_review(session, review)
            session.commit()
            session.refresh(created_review)

        message = {
            "review_id": str(created_review.id),
            "review_bytes": base64.b64encode(
                created_review.review_data.encode()
            ).decode("utf-8"),
        }

        await rabbitmq_pool.publish_message(json.dumps(message))

        return created(created_review)

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while creating review: {error}")
        return server_error(error)


def core_get_review_by_id(request: Request, id: uuid.UUID):
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
        repository: ReviewRepository = request.app.state.review_repository
        with repository.sessionmaker() as session:
            review = repository.get_review_by_id(session, id)

        if review:
            return success(review)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching review with id {id}: {error}")
        return server_error(error)


def core_get_reviews(request: Request):
    """Busca no banco de dados todas as avaliações.

    Args:
    request: Instância de fastapi.Request

    Returns:
    sucesso: Lista, do tipo Json, com todas as avaliações
    não_encontrado: Retorno padrão caso nenhuma entrada seja encontrada no banco de dados
    erro_servidor: Mensagem de erro
    """
    try:
        repository: ReviewRepository = request.app.state.review_repository
        with repository.sessionmaker() as session:
            reviews = repository.get_reviews(session)

        if reviews:
            return success(reviews)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching reviews: {error}")
        return server_error(error)


def core_get_classification_count(request: Request, start_date, end_date):
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
        repository: ReviewRepository = request.app.state.review_repository
        with repository.sessionmaker() as session:
            result = repository.get_classification_count(session, start_date, end_date)

        classification_mapping = {"POS": 0, "NEG": 0, "NEU": 0}
        for classification, count in result:
            classification_mapping[classification] = count

        report = {
            "positiva": classification_mapping["POS"],
            "negativa": classification_mapping["NEG"],
            "neutra": classification_mapping["NEU"],
        }

        if report:
            return success(report)
        return not_found()

    except Exception as exc:
        error = str(exc)
        logger.error(f"Error while fetching report: {error}")
        return server_error(error)
