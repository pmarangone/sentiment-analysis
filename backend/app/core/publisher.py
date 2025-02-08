import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool
from app.config import RABBITMQ_URI
from app.utils.logger import get_logger

logger = get_logger(__name__)


class RabbitMQPool:
    def __init__(self, pool_size: int):
        self.uri = RABBITMQ_URI
        self.pool_size = pool_size
        self.connection_pool = None
        self.channel_pool = None

    async def init_pool(self):
        """Inicializa a conexão com RabbitMQ e uma pool de conexões."""

        # TODO: handle error if connection fails
        async def get_connection() -> AbstractRobustConnection:
            return await aio_pika.connect_robust(self.uri)

        self.connection_pool = Pool(get_connection, max_size=self.pool_size)

        async def get_channel() -> aio_pika.Channel:
            async with self.connection_pool.acquire() as connection:
                return await connection.channel()

        self.channel_pool = Pool(get_channel, max_size=self.pool_size * 10)

        logger.info(
            f"RabbitMQ connection and channel pools initialized with {self.pool_size} connections."
        )

    async def publish_message(
        self, message_body: str, queue_name: str = "sentiment_analysis_queue"
    ):
        """Publica uma mensagem para a fila especificada do RabbitMQ
        
        Args:
        message_body: O corpo da mensagem a ser enviada para a fila.
        
        Raises:
        RuntimeError: Caso não exista uma conexão ativa ou um canal ativo para a pool.
        """

        if not self.connection_pool or not self.channel_pool:
            raise RuntimeError(
                "RabbitMQ pools are not initialized. Call init_pool() first."
            )

        # TODO: handle error, raise custom exception
        async with self.channel_pool.acquire() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body.encode()),
                routing_key=queue_name,
            )
