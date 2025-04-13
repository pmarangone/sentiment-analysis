FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    python3.11-venv \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
COPY . /app
WORKDIR /app

RUN python3 -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

RUN uv sync --frozen --no-cache --python python3.11

CMD ["/app/.venv/bin/celery", "-A", "app.celery_app", "worker", "-P", "prefork", "--loglevel=info", "--task-events", "--queues=sentiment-analysis", "--concurrency", "3"]