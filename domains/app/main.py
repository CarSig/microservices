from fastapi import FastAPI,Response
from app.routes.emails import router as emails_router
from app.routes.breach_router import router as breach_router
from app.routes.store_to_db import router as store_to_db_router
from app.routes.certs import router as certs_router
import httpx
from contextlib import asynccontextmanager
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.request_duration import add_timing_header
from app.middleware.metrics import MetricsMiddleware 
from prometheus_client import generate_latest

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = httpx.AsyncClient()
    yield
    await app.client.aclose()

app = FastAPI(lifespan=lifespan)    
app.middleware("http")(add_timing_header)
app.add_middleware(MetricsMiddleware)


app.include_router(emails_router)
app.include_router(breach_router)
app.include_router(store_to_db_router)
app.include_router(certs_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index() -> str:
    print("welcome")

    return 'welcome to the Items API'

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8200,
        reload=True
    )