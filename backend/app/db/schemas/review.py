from sqlalchemy import Column, Date, ForeignKey, String, JSON
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import relationship
import uuid

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
    classified_at: Data mais recente na qual a predição foi feita.
    Utilizada para refazer as predições feitas por um modelo anterior.

    Scores: Podem ser usados para agregar sentimento e gerar relatórios mais detalhados.
    pos_score: Refere-se ao valor de sentimento 'positivo' retornado na classificação mais recente.
    neg_score: Refere-se ao valor de sentimento 'negativo' retornado na classificação mais recente.
    neu_score: Refere-se ao valor de sentimento 'neutro' retornado na classificação mais recente.
    """

    __tablename__ = "reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
    )
    review_date = Column(Date, nullable=False)
    review_data = Column(String, nullable=False)
    classification = Column(
        ENUM("positive", "negative", "neutral", name="classification_enum"),
        nullable=True,
    )
    classified_at = Column(Date, nullable=True)
    sentiment_scores = Column(JSON, nullable=True)

    customer = relationship("Customer", back_populates="reviews")
