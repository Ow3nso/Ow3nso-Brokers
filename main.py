import uvicorn
from fastapi import FastAPI
from apis.authentication.views import auth_router
from fastapi_jwt_auth import AuthJWT
from apis.authentication.schemas import Settings

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)

if __name__ == '__main__':
    app.run(debug=True, port=8000)