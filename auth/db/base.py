from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import models so Alembic detects them
from db.models import User 
