"""Função utilitária de logging para ser usada através do projeto.
Recebe `__name__`, que será o nome do arquivo inicializando a classe de logging.

Exemplo:

  logger = get_logger(__name__)
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_logger(name):
    return logging.getLogger(name)
