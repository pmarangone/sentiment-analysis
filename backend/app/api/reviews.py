from datetime import datetime
from typing import Annotated
import uuid
from fastapi import (
    APIRouter,
    Query,
    Request,
)

from app.core.core import (
    core_create_review_celery,
    core_create_reviews_many,
    core_get_review_by_id,
    core_get_reviews,
    core_get_classification_count,
)
from app.models.review import RequestReviewModel, RequestReviewsManyModel
from app.utils.logger import get_logger

from app.db.session import PostgresDep


logger = get_logger(__name__)
reviews_router = APIRouter(prefix="/reviews")


@reviews_router.get("/")
async def get_reviews(request: Request, db_session: PostgresDep):
    """Retorna todas as avaliações.

    Args:
    request: Instância de fastapi.Request
    """
    return await core_get_reviews(db_session)


@reviews_router.post("/celery")
async def post_review_celery(
    request: Request,
    review: RequestReviewModel,
    db_session: PostgresDep,
):
    """Cria a avaliação no banco de dados e envia a avaliação e o ID da entrada
    no banco de dados para o consumidor.

    Args:
    request: Instância de fastapi.Request.
    review: Instância de RequestReviewModel.
    Corpo da requisição esperado:
    {
        "customer_name": "Nome",
        "review_date": "2025-01-01",
        "review_data": "Avaliação"
    }

    Returns:
    A entrada do usuário tal como foi criada no banco de dados.
    """
    return await core_create_review_celery(db_session, review)


@reviews_router.post("/many")
async def post_reviews_many(
    request: Request,
    reviews: RequestReviewsManyModel,
    db_session: PostgresDep,
):
    return await core_create_reviews_many(db_session, reviews)


@reviews_router.get("/report")
async def get_reviews_report(
    request: Request,
    start_date: Annotated[datetime, Query()],
    end_date: Annotated[datetime, Query()],
    db_session: PostgresDep,
):
    """Gera um relatório do número de avaliações classificadas como positivas, negativas ou neutras
    entre as datas fornecidas (inclusiva).

    Args:
    request: Instância de fastapi.Request.
    start_date: A data inicial da busca.
    end_date: A data final da busca.

    Returns:
    Lista, do tipo Json, com todas as avaliações feitas entre a data inicial e data final.
    """
    return await core_get_classification_count(db_session, start_date, end_date)


@reviews_router.get("/{id}")
async def get_review_by_id(request: Request, id: uuid.UUID, db_session: PostgresDep):
    """Retorna a avaliação referente ao ID, caso exista.

    Args:
    request: Instância de fastapi.Request.
    id: Instância uuid.UUID referente a avaliação.

    Returns:
    A avaliação referente ao ID ou retorna um erro.
    """
    return await core_get_review_by_id(db_session, id)
