import uuid
from pydantic import BaseModel, Field


class BaseReviewModel(BaseModel):
    """Modelo base para a criação de uma avaliação.

    Attributes:
    customer_name: Nome do usuário.
    review_date: Data na qual o usuário fez a avaliação.
    review_data: Avaliação feita pelo usuário.
    """

    customer_name: str = Field(...)
    review_date: str = Field(...)
    review_data: str = Field(...)


class ReviewModel(BaseReviewModel):
    """Modelo de avaliação guardada no banco de dados.

    Attributes:
    id: uuid.UUID, gerado pelo banco de dados.
    customer_name: Nome do usuário.
    review_date: Data na qual o usuário fez a avaliação.
    review_data: Avaliação feita pelo usuário.
    classification: Predição feita pelo modelo.
    classified: Valor booleano usado para desambiguar quais avaliações foram preditas.
    classified_at: Data mais recente da predição.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    classification: str = Field(...)
    classified: bool = Field(...)
    classified_at: str = Field(...)
