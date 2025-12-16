from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so Alembic detects them
from app.db.models.domain_breach import DomainBreach 
