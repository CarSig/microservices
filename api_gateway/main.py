from fastapi import FastAPI, Request, Response
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# backend base URL inside Docker network
EXPOSED_OR_NOT_URL = "http://exposed_or_not_api:5000"


# @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
# async def proxy(full_path: str, request: Request):
#     """Proxy ANY request dynamically to the backend service."""
    
#     url = f"{EXPOSED_OR_NOT_URL}/{full_path}"
    
#     # Extract method, headers, query params, body
#     method = request.method
#     headers = dict(request.headers)
#     params = dict(request.query_params)
    
#     body = await request.body()
    
#     async with httpx.AsyncClient() as client:
#         backend_response = await client.request(
#             method=method,
#             url=url,
#             headers=headers,
#             params=params,
#             content=body
#         )
    
#     # Return raw response from backend
#     return Response(
#         content=backend_response.content,
#         status_code=backend_response.status_code,
#         headers=dict(backend_response.headers),
#         media_type=backend_response.headers.get("content-type")
#     )


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
    return await proxy(request, f"{EXPOSED_OR_NOT_URL}/")


@app.get("/health")
async def health(request: Request):
    return await proxy(request, f"{EXPOSED_OR_NOT_URL}/health")


@app.get("/breaches")
async def breaches(request: Request):
    return await proxy(request, f"{EXPOSED_OR_NOT_URL}/breaches")


@app.get("/breaches/{breach_id}")
async def breach(request: Request, breach_id: str):
    return await proxy(request, f"{EXPOSED_OR_NOT_URL}/breaches/{breach_id}")


@app.get("/emails/{email}")
async def emails(email: str, request: Request):
    return await proxy(request, f"{EXPOSED_OR_NOT_URL}/emails/{email}")


@app.get("/analytics/{email}")
async def analytics(email: str, request: Request):
    return await proxy(request, f"{EXPOSED_OR_NOT_URL}/analytics/{email}")


@app.post("/store/breach")
async def store_breach(request: Request):
    return await proxy(request, f"{EXPOSED_OR_NOT_URL}/store/breach")