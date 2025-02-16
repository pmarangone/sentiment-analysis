from typing import Annotated
import uuid
from fastapi import (
    APIRouter,
    Query,
    Request,
)

from app.core.core import (
    core_create_review,
    core_create_review_celery,
    core_get_review_by_id,
    core_get_reviews,
    core_get_classification_count,
)
from app.models.review import RequestReviewModel
from app.utils.logger import get_logger


logger = get_logger(__name__)
reviews_router = APIRouter(prefix="/reviews")


@reviews_router.get("/")
async def get_reviews(request: Request):
    """Retorna todas as avaliações.

    Args:
    request: Instância de fastapi.Request
    """
    return core_get_reviews(request)


@reviews_router.post("/")
async def post_review(request: Request, review: RequestReviewModel):
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
    return await core_create_review(request, review)


@reviews_router.post("/celery")
async def post_review_celery(request: Request, review: RequestReviewModel):
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
    return await core_create_review_celery(request, review)


@reviews_router.get("/report")
async def get_reviews_report(
    request: Request,
    start_date: Annotated[str, Query()],
    end_date: Annotated[str, Query()],
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
    return core_get_classification_count(request, start_date, end_date)


@reviews_router.get("/{id}")
async def get_review_by_id(request: Request, id: uuid.UUID):
    """Retorna a avaliação referente ao ID, caso exista.

    Args:
    request: Instância de fastapi.Request.
    id: Instância uuid.UUID referente a avaliação.

    Returns:
    A avaliação referente ao ID ou retorna um erro.
    """
    return core_get_review_by_id(request, id)
