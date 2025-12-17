from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.breach_schema import Breaches,Breach
from app.services import breach_service

# from fastapi import APIRouter,Request

# from app.db.session import get_db
# from fastapi import Depends
# from sqlalchemy.orm import Session
# from app.schemas.breach_schema import Breaches,Breach
# from app.repositories import breach_repo

router = APIRouter(
    prefix="/breaches",
    tags=["Breaches"]
)


@router.get("", response_model=Breaches)
async def get_breaches(db: AsyncSession = Depends(get_db)):
    return await breach_service.get_all_breaches(db)

@router.get("/{breach_id}", response_model=Breach)
async def get_breach(
    breach_id: str,
    db: AsyncSession = Depends(get_db),
):
    return await breach_service.get_breach_by_domain(db, breach_id)

# @router.get("", response_model=Breaches)
# @router.get("/", response_model=Breaches)
# async  def get_breaches(db: Session = Depends(get_db)):
#     breaches = await breach_repo.get_all_breaches(db)
#     return Breaches(exposedBreaches=[Breach.model_validate(b) for b in breaches])



# @router.get("/{breach_id}",response_model=Breaches | dict)
# async  def get_breach(breach_id: str, db: Session = Depends(get_db)):
#     breach = await breach_repo.get_breach_by_domain(db, breach_id)
#     if breach:
#         return Breaches(exposedBreaches=[Breach.model_validate(breach)])
#     return {"message": "Breach not found"}
