from app.utils.logger import get_logger
from app.config import POOL_SIZE
from app.core.client_rabbitmq import RabbitMQPool

logger = get_logger(__name__)


async def main():
    try:
        rabbitmq_pool = RabbitMQPool(pool_size=int(POOL_SIZE))

        await rabbitmq_pool.init_pool()

        await rabbitmq_pool.listen_to_rabbitmq()

    # TODO: handle shutdown gracefully
    except Exception as e:
        logger.error(f"Consumer encountered an error: {e}")
    finally:
        logger.info("Shutting down the consumer...")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
