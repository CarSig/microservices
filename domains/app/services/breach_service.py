from fastapi import HTTPException
from app.schemas.breach_schema import Breaches, Breach,BreachSmall
from app.repositories import breach_repo
from app.utils.redis_cache_db import redis_cache_db

from sqlalchemy.orm import Session



base_url = "https://api.xposedornot.com/v1/"


async def save_breach_if_not_exists(db, breach: Breach):
    existing = await breach_repo.get_by_breach_id(db, breach.breach_id)
    if existing:
        return existing

    data = breach.to_sqlalchemy()
    return await breach_repo.create(db, data)



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


# @redis_cache_db(ttl=24 * 60 * 3600)
async def get_all_breaches(db):
    rows = await breach_repo.get_all(db)
    return Breaches(
        exposedBreaches=[
            BreachSmall.model_validate(r)
            for r in rows
        ]
    )


# @redis_cache_db(ttl=24 * 60 * 3600)
async def get_breach_by_domain(db, domain: str):
    row = await breach_repo.get_by_domain(db, domain)
    if not row:
        return None
    return Breach.model_validate(row)
