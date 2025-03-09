"""Arquivo principal para a inicialização da aplicação.

1. Inicializa a API, passando como parâmetro `lifespan`.
2. Adiciona CORS. Nesse caso, permite todas requisições.
3. Adiciona os endpoints da API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.api import reviews_router
from app.utils import get_logger
from prometheus_client import make_asgi_app

from app.db.session import lifespan


logger = get_logger(__name__)


app = FastAPI(title="Sentiment Analysis", lifespan=lifespan)


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
