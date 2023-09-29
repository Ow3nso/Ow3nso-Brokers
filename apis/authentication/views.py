from fastapi import APIRouter, Depends, status
from apis.authentication.database import Session, engine
from apis.authentication.schemas import SignUpModel, LoginModel
from apis.authentication.models import User
from apis.authentication.database import Session, engine
from apis.authentication.schemas import SignUpModel  # noqa: F811
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash , check_password_hash
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT

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
async def getusers(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access token"
        )
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.email==current_user).first()
    if user.is_staff:
        try:
            users = session.query(User).all()
            return jsonable_encoder(users)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                detail="unauthorized access"
            )

@auth_router.post("/login", status_code=200)
async def loginuser(user:LoginModel, Authorize:AuthJWT=Depends()):
    db_user=session.query(User).filter(User.email==user.email).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.email)
        refresh_token = Authorize.create_refresh_token(subject=db_user.email)

        response={
            "access":access_token,
            "refresh":refresh_token
        }
        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Username or password"
        )

@auth_router.get("refresh")
async def refresh_token(Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_refresh_token_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide a refresh token"
        )
    
    current_user = Authorize.get_jwt_identity()
    access_token = Authorize.create_access_token(subject=current_user)
    return jsonable_encoder({"access":access_token})