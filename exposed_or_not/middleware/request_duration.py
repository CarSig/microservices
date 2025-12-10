import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

async def add_timing_header(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start
    ms = round(duration * 1000, 2)

    print(f"[{request.method}] {request.url.path} took {ms} ms")

    response.headers["X-Process-Time-ms"] = str(ms)

    return response

