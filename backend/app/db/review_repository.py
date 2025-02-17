from sqlalchemy import create_engine, exc, text
from sqlalchemy.orm import sessionmaker

from app.db.schemas import Base
from app.db.schemas.review import ReviewSchema

from app.models.review import CreateReviewModel
from app.utils import get_logger

logger = get_logger(__name__)


class ReviewRepository:
    def __init__(self, url):
        """Inicializa a conexão com o banco de dados e um gerador de sessões.

        Args:
        url: URL para a conexão com o banco de dados, ex: postgresql+psycopg://user:password@localhost/database

        Raises:
        Exception: Caso a criação da conexão falhe
        """
        logger.info("Creating database connection")

        # try:
        #     self.engine = create_engine(url)
        #     self.sessionmaker = sessionmaker(
        #         autocommit=False, autoflush=False, bind=self.engine
        #     )

        # except Exception as exc:
        #     error = str(exc)
        #     logger.error(f"Error occurred: {error}")
        #     raise error

    def initialize_schema(self, engine):
        """Inicializa as tabelas no banco de dados."""
        logger.info("Creating database schemas")
        Base.metadata.create_all(bind=engine)

    def get_reviews(self, session):
        """Busca todas as avaliações no banco de dados.

        Args:
        session: Instância de sqlalchemy.orm.sessionmaker, responsável por gerenciar uma sessão
        do banco de dados.

        Returns: Todas as avaliações guardadas no banco de dados ou nenhum.
        """
        return session.query(ReviewSchema).all()

    def get_review_by_id(self, session, review_id: str) -> ReviewSchema:
        """Busca uma avaliação no banco de dados, filtrada por ID.

        Args:
        session: Instância de sqlalchemy.orm.sessionmaker, responsável por gerenciar uma sessão
        do banco de dados.
        review_id: uuid.UUID, o ID da avaliação.

        Returns: Avaliação feita ou nenhum.
        """
        return session.query(ReviewSchema).filter_by(id=review_id).first()

    def get_classification_count(self, session, start_date, end_date):
        """Conta todas avaliações, com predição, que foram feitas entre data inicial e data final.

        Args:
        start_date: Data inicial da busca.
        end_date: Data final da busca.

        Returns: Relatório com contagem das avaliações classificadas como positiva, negativa ou neutra.
        """
        query = text("""
            SELECT classification, COUNT(*) FROM reviews 
            WHERE classified_at IS NOT NULL
            AND review_date BETWEEN :start_date AND :end_date 
            GROUP BY classification;
        """)

        return session.execute(
            query, {"start_date": start_date, "end_date": end_date}
        ).fetchall()

    def create_review(self, session, review: CreateReviewModel) -> ReviewSchema:
        """Cria uma nova entrada no banco de dados.

        Args:
        review: Instância de BaseReviewModel.

        Returns: Entrada criada no banco de dados, do tipo ReviewSchema.
        """
        new_review = ReviewSchema(**review.model_dump())
        session.add(new_review)
        return new_review
