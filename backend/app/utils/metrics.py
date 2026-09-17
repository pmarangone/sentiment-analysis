from prometheus_client import Counter, Gauge, Histogram
import psutil

REQUEST_DB_DURATION_SECONDS = Histogram(
    "db_request_duration_seconds", "Database request duration in seconds", ["operation"]
)


##### API
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP Request Duration",
    ("method", "status", "path"),
)

REQUEST_COUNT = Counter(
    "http_request_total", "Total HTTP Requests", labelnames=("method", "status", "path")
)

REQUEST_SIZE_HISTOGRAM = Histogram(
    "request_size_bytes", "Size of incoming requests in bytes"
)
RESPONSE_SIZE_HISTOGRAM = Histogram(
    "response_size_bytes", "Size of outgoing responses in bytes"
)


# System metrics
CPU_USAGE = Gauge("process_cpu_usage", "Current CPU usage in percent")
MEMORY_USAGE = Gauge("process_memory_usage_bytes", "Current memory usage in bytes")


def update_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.Process().memory_info().rss)
