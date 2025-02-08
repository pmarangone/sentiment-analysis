from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.api import reviews_router
from app.core.publisher import RabbitMQPool
from app.db import ReviewRepository
from app.utils import get_logger
from app.config import DATABASE_URL, POOL_SIZE

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.review_repository = ReviewRepository(DATABASE_URL)
    app.state.review_repository.initialize_schema()

    app.state.rabbitmq_pool = RabbitMQPool(pool_size=int(POOL_SIZE))
    await app.state.rabbitmq_pool.init_pool()

    yield

    logger.info("Application shutdown")


app = FastAPI(title="Sentiment Analysis", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reviews_router)
