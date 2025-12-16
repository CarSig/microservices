from fastapi import APIRouter,Request,HTTPException
from app.schemas.email_schema import EmailBreachAnalytics, EmailBreaches,ErrorResponse

base_url = "https://api.xposedornot.com/v1"
XON_API = f"{base_url}/check-email"
XON_breach_analytics = f'{base_url}/breach-analytics?email='

async def fetch_email_breaches(client, email: str) -> EmailBreaches | ErrorResponse:
    response = await client.get(f"{XON_API}/{email}")
    data = response.json()
    if "detail" in data:
        raise HTTPException(
            status_code=response.status_code,
            detail=data["detail"].get("error", "Unknown error from XON API")
        )
    return EmailBreaches(**data)


async def fetch_email_breach_analytics(client, email: str) -> EmailBreachAnalytics:
    response = await client.get(f"{XON_breach_analytics}{email}")
    data = response.json()
    print(data)
    if "detail" in data:
        raise HTTPException(
            status_code=response.status_code,
            detail=data["detail"].get("error", "Unknown error from XON API")
        )
    return EmailBreachAnalytics(**data)


