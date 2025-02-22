from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.schemas import Base
from app.db.schemas.customer import Customer
from app.models.customer import CustomerModel
from app.utils import get_logger

logger = get_logger(__name__)


class CustomerRepository:
    def __init__(self, url):
        """Inicializa a conexão com o banco de dados e um gerador de sessões.

        Args:
        url: URL para a conexão com o banco de dados.
        """
        # logger.info("Creating database connection")
        # try:
        #     self.engine = create_engine(url)
        #     self.sessionmaker = sessionmaker(
        #         autocommit=False, autoflush=False, bind=self.engine
        #     )
        # except Exception as exc:
        #     logger.error(f"Error occurred: {str(exc)}")
        #     raise exc

    def initialize_schema(self, engine):
        """Inicializa as tabelas no banco de dados."""
        logger.info("Creating database schemas")
        Base.metadata.create_all(bind=engine)

    def get_customers(self, session):
        """Busca todos os clientes no banco de dados."""
        return session.query(Customer).all()

    def get_customer_by_name(self, session, customer_name: str) -> Customer:
        """Busca um cliente pelo name."""
        return session.query(Customer).filter_by(name=customer_name).first()

    def create_customer(self, session, customer: str) -> Customer:
        """Cria um novo cliente no banco de dados."""
        new_customer = Customer(name=customer)
        session.add(new_customer)
        return new_customer

    # def get_customer_or_create(self, session, customer_name: str) -> Customer:
    #     customer = self.get_customer_by_name(session, customer_name)
    #     if customer:
    #         return customer
    #     new_customer = self.create_customer(sesison, customer=)
