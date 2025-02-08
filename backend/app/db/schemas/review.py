import uuid
from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.schemas import Base


class ReviewSchema(Base):
    """Tabela das classificações dos usuários
    
    Attributes:
    id: uuid.uuid4, gerado pelo banco de dados ao ser criada uma nova entrada.
    customer_name: Nome do usuário que fez a avaliação.
    review_date: Data na qual o usuário fez a avaliação.
    review_data: Avaliação feita pelo usuário.
    classification: Predição feita pelo modelo de aprendizagem.
    classified: Campo usado para desambiguar se foi feita uma predição para a avaliação.
    Ao invés de checar se 'classification' está vazio, esse campo é usado.
    Adicionando index a coluna, temos uma maior performance na busca por avaliações com ou sem predição.
    classifiedAt: Data mais recente na qual a predição foi feita.
    Utilizada para refazer as predições feitas por um modelo anterior. 
    """
    __tablename__ = "reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    customer_name = Column(String, nullable=False)
    # TODO: change this from String to Date (not DateTime)
    review_date = Column(String, nullable=False)
    review_data = Column(String, nullable=False)
    # Updated asynchronously
    # TODO: change this from string to int, save some bytes of storage
    classification = Column(String, default="")
    # Retries
    classified = Column(Boolean, default=False, nullable=False, index=True)
    # TODO: add classifiedAt - rerun classifications if a better model was found.
