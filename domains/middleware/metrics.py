from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware

REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "path", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Latency", ["method", "path"]
)

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        method = request.method
        path = request.url.path

        with REQUEST_LATENCY.labels(method=method, path=path).time():
            response = await call_next(request)

        REQUEST_COUNT.labels(
            method=method,
            path=path,
            status=response.status_code
        ).inc()

        return response
