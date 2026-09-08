import os

DATABASE_URL = os.environ.get("DATABASE_URL")
POSTGRES_POOL_SIZE = int(os.environ.get("POSTGRES_POOL_SIZE", "10"))
RABBITMQ_URI = os.environ.get("RABBITMQ_URI")
