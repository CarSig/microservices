from fastapi import APIRouter,Request
# from schemas.breach_schema import Breaches,Breach

# from repositories import breach_repo
from fastapi import Depends
from db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# @router.get("/login")
# @router.get("/register")
# @router.get("/logout")
# @router.get("/introspect")
# @router.get("/health")




