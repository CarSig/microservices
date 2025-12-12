from fastapi import HTTPException
from schemas.breach_schema import Breaches
from repositories.breach_repo import save_breach_if_not_exists
from sqlalchemy.orm import Session
base_url = "https://api.xposedornot.com/v1/"




async def process_api_response(client, db: Session):
    """
    Takes raw JSON from the external API,
    validates + transforms it into a BreachSchema,
    then stores it in the database only if it does not already exist.
    """
    # Parse + validate + convert breachedDate -> date
    breaches = await fetch_all_breaches(client) 
    saved_items = []
    for breach in breaches.exposedBreaches:  # iterate the list
        saved = save_breach_if_not_exists(db, breach)
        saved_items.append(saved)

    return saved_items



async def fetch_all_breaches(client) -> Breaches:
    response = await client.get(f"{base_url}/breaches")
    data = response.json()
    if "detail" in data:
        raise HTTPException(
            status_code=response.status_code,
            detail=data["detail"].get("error", "Unknown error from XON API")
        )
  
    return Breaches(**data)  
