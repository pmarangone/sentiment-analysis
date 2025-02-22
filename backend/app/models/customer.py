from datetime import date
import uuid
from pydantic import BaseModel, Field


class BaseCustomerModel(BaseModel):
    """Modelo base para a criação de um usuário.

    Attributes:
    name: Nome do usuário.
    """

    name: str = Field(...)


class CustomerModel(BaseCustomerModel):
    """Modelo de customer guardada no banco de dados.

    Attributes:
    id: uuid.UUID, gerado pelo banco de dados.
    name: Nome do usuário.

    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(...)
