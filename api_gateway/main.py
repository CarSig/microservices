from fastapi import FastAPI, Request, Response
import httpx
from fastapi.middleware.cors import CORSMiddleware
import socket
import os
from urllib.parse import quote

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def resolve_or_default(host: str, port: int, fallback: str) -> str:
    """Try to resolve <host>. If it doesn't exist, use fallback URL."""
    try:
        socket.gethostbyname(host)   # check if host exists (Docker)
        return f"http://{host}:{port}"
    except socket.gaierror:
        return fallback

DOMAINS_URL = os.getenv("DOMAINS_URL")

if not DOMAINS_URL:
    DOMAINS_URL = "http://localhost:5000"
    print("DOMAINS_URL not set, defaulting to localhost")




async def proxy(request: Request, url: str):
    method = request.method
    headers = dict(request.headers)
    params = dict(request.query_params)
    body = await request.body()

    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            content=body
        )

    return Response(
        content=resp.content,
        status_code=resp.status_code,
        media_type=resp.headers.get("content-type")
    )


@app.get("/")
async def root(request: Request):
    return await proxy(request, f"{DOMAINS_URL}/")


@app.get("/health")
async def health(request: Request):
    return await proxy(request, f"{DOMAINS_URL}/health")


@app.get("/breaches")
async def breaches(request: Request):
    return await proxy(request, f"{DOMAINS_URL}/breaches")


@app.get("/breaches/{breach_id}")
async def breach(request: Request, breach_id: str):
    return await proxy(request, f"{DOMAINS_URL}/breaches/{breach_id}")


@app.get("/emails/{email}")
async def emails(email: str, request: Request):
    return await proxy(request, f"{DOMAINS_URL}/emails/{email}")


@app.get("/emails/analytics/{email}")
async def analytics(email: str, request: Request):
    safe_email = quote(email)

    return await proxy(request, f"{DOMAINS_URL}/emails/analytics/{safe_email}")


@app.post("/store/breach")
async def store_breach(request: Request):
    return await proxy(request, f"{DOMAINS_URL}/store/breach")