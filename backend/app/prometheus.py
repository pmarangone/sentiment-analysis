import psutil


from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
)


REQUEST_COUNT = Counter(
    "http_request_total", "Total HTTP Requests", ["method", "status", "path"]
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ["method", "status", "path"],
)
REQUEST_IN_PROGRESS = Gauge(
    "http_requests_in_progress", "HTTP Requests in progress", ["method", "path"]
)

# System metrics
CPU_USAGE = Gauge("process_cpu_usage", "Current CPU usage in percent")
MEMORY_USAGE = Gauge("process_memory_usage_bytes", "Current memory usage in bytes")


def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)
