"""Função utilitária de logging para ser usada através do projeto.
Recebe `__name__`, que será o nome do arquivo inicializando a classe de logging.

Exemplo:

  logger = get_logger(__name__)
"""

import logging
from multiprocessing import Queue
import os

from logging_loki import LokiQueueHandler


def get_logger(name):
    endpoint = os.environ.get("LOKI_ENDPOINT")
    if endpoint is None:
        raise Exception("LOKI_ENDPOINT environment variable is not set")

    environment = os.environ.get("ENV", "PROD")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(name)

    if environment == "PROD":
        try:
            loki_logs_handler = LokiQueueHandler(
                Queue(-1),
                url=endpoint,
                tags={"application": "fastapi"},
                version="1",
            )

            logger.addHandler(loki_logs_handler)
        except Exception as exc:
            logger.error(f"Error occurred: {exc}")
            raise exc

    return logger
