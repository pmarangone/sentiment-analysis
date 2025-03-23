"""Arquivo principal para a inicialização da aplicação.

1. Inicializa a API, passando como parâmetro `lifespan`.
2. Adiciona CORS. Nesse caso, permite todas requisições.
3. Adiciona os endpoints da API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api import reviews_router
from app.utils.decorators import monitor_requests_middleware
from app.utils.logger import get_logger
from app.utils.metrics_route import metrics_router

from app.db.session import lifespan


logger = get_logger(__name__)


app = FastAPI(title="Sentiment Analysis", lifespan=lifespan)

app.middleware("http")(monitor_requests_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reviews_router)
app.include_router(metrics_router)
