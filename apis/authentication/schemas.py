from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
    id:Optional[int]
    firstname:str
    lastname:str
    email:str
    id_number:int
    country:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "firstname":"John",
                "lastname":"Doe",
                "email":"johndoe@gmail.com",
                "id_number":12345678,
                "country":"Kenya",
                "password":"password",
                "is_staff":False,
                "is_active":True
            }
        }
    
class Settings(BaseModel):
    authjwt_secret_key:str = '11e2abfce50b4277e360486d61425af91e489da310febd72b1d3deb6496f1489'

class LoginModel(BaseModel):
    email:str
    password:str