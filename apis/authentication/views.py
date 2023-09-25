from fastapi import APIRouter, Depends, status
from apis.authentication.database import Session, engine
from apis.authentication.schemas import SignUpModel
from apis.authentication.models import User
from apis.authentication.database import Session, engine
from apis.authentication.schemas import SignUpModel  # noqa: F811
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash , check_password_hash
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

session = Session(bind=engine)

@auth_router.post("/signup",
        status_code=status.HTTP_201_CREATED
     )
async def signup(user:SignUpModel):

    db_email = session.query(User).filter(User.email==user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with the email already exists"
        )

    db_username = session.query(User).filter(User.id_number==user.id_number).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that id already exists"
        )

    new_user = User(
        firstname = user.firstname, 
        lastname = user.lastname,
        email = user.email, 
        id_number = user.id_number,
        country = user.country,
        password = generate_password_hash(user.password),
        is_staff = user.is_staff,
        is_active = user.is_active
    )

    session.add(new_user)
    session.commit()
    response = {
        "firstname":user.firstname,
        "lastname":user.lastname,
        "email":user.email,
        "id_number":user.id_number,
        "country":user.country,
        "password":user.password,
        "is_staff":user.is_staff,
        "is_active":user.is_active
    }
    return jsonable_encoder(response)

@auth_router.get("/signup")
async def getusers():
    users = session.query(User).all()
    return jsonable_encoder(users)

