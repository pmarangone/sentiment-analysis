FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["/app/.venv/bin/python", "worker.py"]