import aio_pika
from aio_pika.abc import AbstractRobustConnection
from aio_pika.pool import Pool
from app.config import RABBITMQ_URI
from app.utils.logger import get_logger
from app.core.core import predict_sentiment

logger = get_logger(__name__)


class RabbitMQPool:
    def __init__(self, pool_size: int):
        self.uri = RABBITMQ_URI
        self.pool_size = pool_size
        self.connection_pool = None
        self.channel_pool = None

    async def init_pool(self):
        """Inicializa a conexão com RabbitMQ e uma pool de conexões."""

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

    async def listen_to_rabbitmq(self):
        """Escuta a fila do RabbitMQ e processa as mensagens recebidas.

        Raises:
        RuntimeError: Caso não exista uma conexão ativa ou um canal ativo para a pool.
        """
        if not self.connection_pool or not self.channel_pool:
            raise RuntimeError("RabbitMQ pools are not initialized.")

        async with self.channel_pool.acquire() as channel:
            queue = await channel.declare_queue(
                "sentiment_analysis_queue", durable=True
            )

            async with queue.iterator() as queue_iter:
                logger.info("Listening for messages on 'sentiment_analysis_queue'")

                async for message in queue_iter:
                    try:
                        await predict_sentiment(message)

                        await message.ack()
                        logger.info("Message acknowledged successfully.")

                    except Exception as ex:
                        logger.error(f"Unhandled error occurred: {ex}")
                        await message.nack(requeue=False)  # Retry
