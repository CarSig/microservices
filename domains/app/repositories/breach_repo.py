from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.domain_breach import DomainBreach
from app.schemas.breach_schema import Breach as Breach
from app.utils.redis_cache_db import redis_cache_db

def save_breach_if_not_exists(db: Session, breach: Breach):
    data = breach.to_sqlalchemy()
    # check by unique ID
    stmt = select(DomainBreach).where(DomainBreach.breach_id == data["breach_id"])
    existing = db.scalar(stmt)
    if existing:
        return existing 
    new_breach = DomainBreach(**data)
    db.add(new_breach)
    db.commit()
    db.refresh(new_breach)
    return new_breach

@redis_cache_db(ttl=24*60*3600)
async def get_all_breaches(db: Session):
    stmt = select(DomainBreach)
    x =await db.scalars(stmt)
    rows = x.all()
    results = [Breach.model_validate(b).model_dump() for b in rows]
    return results 

@redis_cache_db(ttl=24*60*3600)
async def get_breach_by_domain(db: Session, domain: str):
    stmt = select(DomainBreach).where(DomainBreach.domain == domain)
    row =await db.scalar(stmt)
    if row:
        return Breach.model_validate(row).model_dump()
    return None
