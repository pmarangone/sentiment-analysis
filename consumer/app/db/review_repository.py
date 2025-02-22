from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import DATABASE_URL
from app.db.schemas import Base
from app.db.schemas.review import ReviewSchema
from app.utils.logger import get_logger

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

        self.engine = create_engine(url)
        self.sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def initialize_schema(self):
        """Inicializa as tabelas no banco de dados."""
        logger.info("Creating database schemas")
        Base.metadata.create_all(bind=self.engine)

    def update_review(self, session, review_id: str):
        """Atualiza a classificação de uma avaliação no banco de dados.

        Args:
            session: Instância de sqlalchemy.orm.sessionmaker, responsável por gerenciar uma sessão
            do banco de dados.
            review_id: ID da avaliação.
        """
        return (
            session.query(ReviewSchema)
            .with_for_update()
            .filter_by(id=review_id)
            .first()
        )


review_repository = ReviewRepository(DATABASE_URL)
review_repository.initialize_schema()
