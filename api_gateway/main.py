from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()

# backend base URL inside Docker network
EXPOSED_OR_NOT_URL = "http://exposed_or_not_api:5000"


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(full_path: str, request: Request):
    """Proxy ANY request dynamically to the backend service."""
    
    url = f"{EXPOSED_OR_NOT_URL}/{full_path}"
    
    # Extract method, headers, query params, body
    method = request.method
    headers = dict(request.headers)
    params = dict(request.query_params)
    
    body = await request.body()
    
    async with httpx.AsyncClient() as client:
        backend_response = await client.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            content=body
        )
    
    # Return raw response from backend
    return Response(
        content=backend_response.content,
        status_code=backend_response.status_code,
        headers=dict(backend_response.headers),
        media_type=backend_response.headers.get("content-type")
    )
