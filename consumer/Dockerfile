FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["/app/.venv/bin/celery", "-A", "app.celery_app", "worker", "-P", "prefork", "--loglevel=info", "--task-events", "--queues=sentiment-analysis", "--concurrency", "3"]