from fastapi import APIRouter, Depends, status
from apis.authentication.database import Session, engine
from apis.authentication.schemas import SignUpModel
from apis.authentication.models import User

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session = Session(bind=engine)

@auth_router.get("/")
async def hello():
    return {"message":"hello world"}