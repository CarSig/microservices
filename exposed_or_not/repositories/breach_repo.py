from sqlalchemy.orm import Session
from sqlalchemy import select
from db.models.domain_breach import DomainBreach
from schemas.breach_schema import Breach as Breach


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

def get_all_breaches(db: Session):
    stmt = select(DomainBreach)
    rows = db.scalars(stmt).all()
    results = [Breach.model_validate(b).model_dump() for b in rows]
    return results 

def get_breach_by_domain(db: Session, domain: str):
    stmt = select(DomainBreach).where(DomainBreach.domain == domain)
    row = db.scalar(stmt)
    if row:
        return Breach.model_validate(row).model_dump()
    return None
