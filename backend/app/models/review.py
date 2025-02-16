from datetime import date
import uuid
from pydantic import BaseModel, Field
from typing import Optional, Dict


class CreateReviewModel(BaseModel):
    """Modelo base para a criação de uma avaliação.

    Attributes:
    customer_id: ID do usuário que fez a avaliação.
    review_date: Data na qual o usuário fez a avaliação.
    review_data: Avaliação feita pelo usuário.
    """

    customer_id: uuid.UUID = Field(...)
    review_date: date = Field(...)
    review_data: str = Field(...)


class RequestReviewModel(BaseModel):
    """Modelo base para a criação de uma avaliação.

    Attributes:
    customer_name: Nome do usuário.
    review_date: Data na qual o usuário fez a avaliação.
    review_data: Avaliação feita pelo usuário.
    """

    customer_name: str = Field(...)
    review_date: date = Field(...)
    review_data: str = Field(...)


class ReviewModel(RequestReviewModel):
    """Modelo de avaliação guardada no banco de dados.

    Attributes:
    id: uuid.UUID, gerado pelo banco de dados.
    classification: Predição feita pelo modelo.
    classified_at: Data mais recente da predição.
    sentiment_scores: Dicionário contendo as pontuações de sentimento (positivo, negativo, neutro).
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    customer_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    review_date: Optional[date] = Field(None)
    review_data: Optional[str] = Field(None)
    classification: Optional[str] = Field(None)
    classified_at: Optional[date] = Field(None)
    sentiment_scores: Optional[Dict[str, float]] = Field(None)
