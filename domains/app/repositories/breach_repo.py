from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.domain_breach import DomainBreach
# from app.schemas.breach_schema import Breach as Breach
# from app.utils.redis_cache_db import redis_cache_db
from sqlalchemy.ext.asyncio import AsyncSession


async def get_by_breach_id(
    db: AsyncSession,
    breach_id: str,
) -> DomainBreach | None:
    stmt = select(DomainBreach).where(DomainBreach.breach_id == breach_id)
    return await db.scalar(stmt)


async def create(
    db: AsyncSession,
    data: dict,
) -> DomainBreach:
    breach = DomainBreach(**data)
    db.add(breach)
    await db.commit()
    await db.refresh(breach)
    return breach


async def get_all(db: AsyncSession) -> list[DomainBreach]:
    # stmt = select(DomainBreach)
    stmt = select(
        DomainBreach.breach_id,
        DomainBreach.breached_date,
        DomainBreach.domain,
        DomainBreach.industry,
        DomainBreach.exposed_records,
    )
    result = await db.execute(stmt)
    # rows = result.all()
    return result.mappings().all()
   


async def get_by_domain(
    db: AsyncSession,
    domain: str,
) -> DomainBreach | None:
    stmt = select(DomainBreach).where(DomainBreach.domain == domain)
    return await db.scalar(stmt)




# def save_breach_if_not_exists(db: Session, breach: Breach):
#     data = breach.to_sqlalchemy()
#     stmt = select(DomainBreach).where(DomainBreach.breach_id == data["breach_id"])
#     existing = db.scalar(stmt)
#     if existing:
#         return existing 
#     new_breach = DomainBreach(**data)
#     db.add(new_breach)
#     db.commit()
#     db.refresh(new_breach)
#     return new_breach

# # @redis_cache_db(ttl=24*60*3600)
# async def get_all_breaches(db: Session):
#     stmt = select(DomainBreach)
#     x =await db.scalars(stmt)
#     rows = x.all()
#     results = [Breach.model_validate(b).model_dump() for b in rows]
#     return results 

# # @redis_cache_db(ttl=24*60*3600)
# async def get_breach_by_domain(db: Session, domain: str):
#     stmt = select(DomainBreach).where(DomainBreach.domain == domain)
#     row =await db.scalar(stmt)
#     if row:
#         return Breach.model_validate(row).model_dump()
#     return None
