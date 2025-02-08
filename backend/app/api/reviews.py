from typing import Annotated
import uuid
from fastapi import (
    APIRouter,
    Query,
    Request,
)

from app.core.core import (
    core_create_review,
    core_get_review_by_id,
    core_get_reviews,
    core_get_classification_count,
)
from app.models.review import BaseReviewModel
from app.utils.logger import get_logger


logger = get_logger(__name__)
reviews_router = APIRouter(prefix="/reviews")


@reviews_router.get("/")
async def get_reviews(request: Request):
    return core_get_reviews(request)


@reviews_router.post("/")
async def post_review(request: Request, review: BaseReviewModel):
    """Cria a avaliação no banco de dados e envia a avaliação e o ID da entrada
    no banco de dados para o consumidor.
    
    Args:
    request: Instância de fastapi.Request
    review: Instância derivada de pydantic.BaseModel, que foi enviado no corpo da requisição.
    Corpo da mensagem esperada: 
    {
        "customer_name": "Name",
        "review_date": "2025-01-01",
        "review_data": "CustomerReviewHere"
    }
    """
    return await core_create_review(request, review)


@reviews_router.get("/report")
async def get_reviews_report(
    request: Request,
    start_date: Annotated[str, Query()],
    end_date: Annotated[str, Query()],
):
    """Gera um relatório do número de avaliações positivas, negativas ou neutras
    feitas entre a data inicial e a data final (inclusiva).

    Args:
    request: Instância de fastapi.Request
    start_date: Query com a data inicial da busca, ex: 2025-01-01
    end_date: Query com a data final da busca, ex: 2025-01-10
    """
    # TODO: o que acontece caso não seja enviado start_date ou end_date? hmmm
    return core_get_classification_count(request, start_date, end_date)


@reviews_router.get("/{id}")
async def get_review_by_id(request: Request, id: uuid.UUID):
    return core_get_review_by_id(request, id)
