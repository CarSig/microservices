from fastapi import FastAPI
from routes.emails import router as emails_router
from routes.breach_router import router as breach_router
from routes.store_to_db import router as store_to_db_router
import httpx
from contextlib import asynccontextmanager
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from middleware.request_duration import add_timing_header

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.client = httpx.AsyncClient()
    yield
    await app.client.aclose()

app = FastAPI(lifespan=lifespan)    
app.middleware("http")(add_timing_header)

app.include_router(emails_router)
app.include_router(breach_router)
app.include_router(store_to_db_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def index() -> str:
    print("welcome")

    return 'welcome to the Items API'



if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8200,
        reload=True
    )