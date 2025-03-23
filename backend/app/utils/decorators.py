import time
from functools import wraps
from fastapi import Request

from fastapi.responses import StreamingResponse

from app.utils.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    REQUEST_SIZE_HISTOGRAM,
    RESPONSE_SIZE_HISTOGRAM,
    REQUEST_DB_DURATION_SECONDS,
)


def monitor_db_operation(operation: str):
    """
    Decorator to monitor the database operation duration and track it with Prometheus.
    :param operation: The type of operation (e.g., 'create', 'select')
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                result = await func(*args, **kwargs)
                duration = time.perf_counter() - start_time
                REQUEST_DB_DURATION_SECONDS.labels(operation=operation).observe(
                    duration
                )
                return result
            except Exception as e:
                raise e

        return wrapper

    return decorator


# TODO: measure time added by adding this
async def monitor_request_response_size(request, response):
    request_size = int(request.headers.get("content-length", 0))
    REQUEST_SIZE_HISTOGRAM.observe(request_size)
    response_body = b"".join([chunk async for chunk in response.body_iterator])
    response_size = len(response_body)
    response = StreamingResponse(
        iter([response_body]),
        status_code=response.status_code,
        headers=dict(response.headers),
    )
    RESPONSE_SIZE_HISTOGRAM.observe(response_size)

    return response


async def monitor_requests_middleware(request: Request, call_next):
    method = request.method
    path = request.url.path

    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    status = response.status_code
    REQUEST_COUNT.labels(method=method, status=status, path=path).inc()
    REQUEST_LATENCY.labels(method=method, status=status, path=path).observe(duration)

    if True:
        response = await monitor_request_response_size(request, response)

    return response
