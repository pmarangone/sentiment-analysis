import os

DATABASE_URL = os.environ.get("DATABASE_URL", None)
POOL_SIZE = os.environ.get("POOL_SIZE")
RABBITMQ_URI = os.environ.get("RABBITMQ_URI")
