from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.breach_service import process_api_response

router = APIRouter(
    prefix="/store",
    tags=["Store"]
)

@router.get("/")
async def index_store() -> str:
    print("welcome")

    return 'welcome to the DB store'

@router.get("/breach")
async def store_breach(request: Request, db: Session = Depends(get_db)):
    print("Storing breach to DB...")
    client = request.app.client
    result = await process_api_response(client,db)
    print(result)
    print("Breach stored.")

    return result