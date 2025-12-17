from pydantic import BaseModel
from app.schemas.email_schema_parts import XposedData,IndustryData,RiskData,DictWithInts
class ErrorResponse(BaseModel):
    Error : str
    email: str | None

    
class BreachMetrics(BaseModel):
    get_details: list[str]
    industry: IndustryData
    passwords_strength: DictWithInts
    risk: RiskData
    xposed_data :XposedData
    yearwise_details: DictWithInts

class Summary (BaseModel):
    site: str    

class ExposedBreach(BaseModel):
    breach:str
    details: str
    domain: str
    industry: str
    logo: str
    password_risk: str
    references:str
    searchable: str
    verified: str
    xposed_data: str
    xposed_date: str
    xposed_records: int
    added: str

class ExposedBreaches(BaseModel):
    breaches_details: list [ExposedBreach]   

class EmailBreachAnalytics(BaseModel):
    BreachMetrics: BreachMetrics
    BreachesSummary: Summary
    ExposedBreaches: ExposedBreaches
    ExposedPastes: dict | None
    PasteMetrics: dict | None
    PastesSummary: dict


    
class EmailBreaches(BaseModel):
    breaches: list[list[str]]
    email: str
    status: str
