"""Arquivo principal para a inicialização da aplicação.

1. Inicializa a API, passando como parâmetro `lifespan`.
2. Adiciona CORS. Nesse caso, permite todas requisições.
3. Adiciona os endpoints da API.
"""

import time
from fastapi import FastAPI, Request, Response
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import (
    generate_latest,
    REGISTRY,
    CONTENT_TYPE_LATEST,
)


from app.api import reviews_router
from app.core.publisher import RabbitMQPool
from app.db import ReviewRepository
from app.db import CustomerRepository
from app.utils import get_logger
from app.config import DATABASE_URL, POOL_SIZE
from prometheus_client import make_asgi_app


logger = get_logger(__name__)


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Inicializa ReviewRepository e RabbitMQPool, guardando as instâncias no estado da aplicação para
#     serem reutilizadas a cada request. Dessa forma, segue-se o Singleton Pattern"""
#     app.state.review_repository = ReviewRepository(DATABASE_URL)
#     app.state.review_repository.initialize_schema()

#     app.state.customer_repository = CustomerRepository(DATABASE_URL)
#     app.state.customer_repository.initialize_schema()

#     app.state.rabbitmq_pool = RabbitMQPool(pool_size=int(POOL_SIZE))
#     await app.state.rabbitmq_pool.init_pool()

#     yield

#     logger.info("Application shutdown")


app = FastAPI(title="Sentiment Analysis")


# @app.middleware("http")
# async def monitor_requests(request: Request, call_next):
#     # method = request.method
#     # path = request.url.path

#     # REQUEST_IN_PROGRESS.labels(method=method, path=path).inc()

#     # start_time = time.time()

#     response = await call_next(request)

#     # duration = time.time() - start_time

#     # status = response.status_code
#     # REQUEST_COUNT.labels(method=method, status=status, path=path).inc()
#     # REQUEST_LATENCY.labels(method=method, status=status, path=path).observe(duration)
#     # REQUEST_IN_PROGRESS.labels(method=method, path=path).dec()

#     return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reviews_router)


metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
