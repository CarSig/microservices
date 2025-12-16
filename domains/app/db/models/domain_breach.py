from sqlalchemy import Column, Integer, String, Boolean, Date, Text, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DomainBreach(Base):
    __tablename__ = "domains_breached"
    id = Column(Integer, primary_key=True, index=True)
    breach_id = Column(String, unique=True, nullable=False)
    domain = Column(String, nullable=False)

    breached_date = Column(Date, nullable=False)
    exposed_data = Column(ARRAY(String), nullable=False)
    exposed_records = Column(Integer)

    exposure_description = Column(Text)
    industry = Column(String)
    logo = Column(String)
    password_risk = Column(String)
    reference_url = Column(String)

    searchable = Column(Boolean)
    sensitive = Column(Boolean)
    verified = Column(Boolean)
