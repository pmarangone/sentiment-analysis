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
        """Initialize the RabbitMQ connection and channel pools."""

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
        self, message_body: str, queue_name: str = "transcription_queue"
    ):
        """Publish a message to the specified queue."""
        if not self.connection_pool or not self.channel_pool:
            raise RuntimeError(
                "RabbitMQ pools are not initialized. Call init_pool() first."
            )

        async with self.channel_pool.acquire() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body.encode()),
                routing_key=queue_name,
            )
