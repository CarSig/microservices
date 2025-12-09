from pydantic import BaseModel, Field
from datetime import datetime, date

class Breach(BaseModel):
    
    breachID: str = Field(alias="breach_id")
    breachedDate: date = Field(alias="breached_date")
    domain: str
    exposedData: list[str] = Field(alias="exposed_data")
    exposedRecords: int | None = Field(alias="exposed_records")
    exposureDescription: str = Field(alias="exposure_description")
    industry: str
    logo: str
    passwordRisk: str = Field(alias="password_risk")
    referenceURL: str | None = Field(alias="reference_url")
    searchable: bool
    sensitive: bool
    verified: bool
    model_config = {
            "from_attributes": True,
            "populate_by_name": True
        }
    def to_sqlalchemy(self):
     
        return {
            "breach_id": self.breachID,
            "domain": self.domain,
            "breached_date": self.breachedDate,
            "exposed_data": self.exposedData,
            "exposed_records": self.exposedRecords,
            "exposure_description": self.exposureDescription,
            "industry": self.industry,
            "logo": self.logo,
            "password_risk": self.passwordRisk,
            "reference_url": self.referenceURL,
            "searchable": self.searchable,
            "sensitive": self.sensitive,
            "verified": self.verified
        }



class Breaches(BaseModel):
    exposedBreaches: list[Breach]


