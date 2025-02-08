import os

REDIS_HOST = os.environ.get("REDIS_HOST")
RABBITMQ_URI = os.environ.get("RABBITMQ_URI")
POOL_SIZE = os.environ.get("POOL_SIZE")
MAX_RETRIES = os.environ.get("MAX_RETRIES")
DATABASE_URL = os.environ.get("DATABASE_URL")
