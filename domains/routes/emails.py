from fastapi import APIRouter,Request
from schemas.email_schema import EmailBreachAnalytics, EmailBreaches,ErrorResponse
from services.emails_service import fetch_email_breaches, fetch_email_breach_analytics




router = APIRouter(
    prefix="/emails",
    tags=["Breached Emails"]
)



@router.get("/")
def index() -> str:
    return 'welcome to the breach4er API'







@router.get("/analytics/{email}", response_model=EmailBreachAnalytics | ErrorResponse)
async def get_email_breach_analytics(request: Request,email: str):
    client = request.app.client
    return await fetch_email_breach_analytics(client, email)    

@router.get("/{email}", response_model=EmailBreaches | ErrorResponse)
async def get_email_breaches(request: Request,email: str):
    client = request.app.client
    return await fetch_email_breaches(client, email)
