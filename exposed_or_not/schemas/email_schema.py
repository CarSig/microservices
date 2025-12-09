from pydantic import BaseModel
class ErrorResponse(BaseModel):
    Error : str
    email: str | None

    
class BreachMetrics(BaseModel):
    get_details: list[str]
    industry: list[list[list[str | int]]]
    passwords_strength: list[dict]
    risk: list[dict]
    xposed_data : list[dict]
    yearwise_details: list[dict]

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
