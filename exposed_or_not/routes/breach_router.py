from fastapi import APIRouter,Request
from schemas.breach_schema import Breaches,Breach

from repositories import breach_repo
from fastapi import Depends
from db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/breaches",
    tags=["Breaches"]
)

@router.get("", response_model=Breaches)
@router.get("/", response_model=Breaches)
async def get_breaches(db: Session = Depends(get_db)):
    breaches =await  breach_repo.get_all_breaches(db)
    return Breaches(exposedBreaches=[Breach.model_validate(b) for b in breaches])



@router.get("/{breach_id}",response_model=Breaches | dict)
async def get_breach(breach_id: str, db: Session = Depends(get_db)):
    breach = await breach_repo.get_breach_by_domain(db, breach_id)
    if breach:
        return Breaches(exposedBreaches=[Breach.model_validate(breach)])
    return {"message": "Breach not found"}
