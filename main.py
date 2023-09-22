import uvicorn
from fastapi import FastAPI
from apis.authentication.views import auth_router

app = FastAPI()

app.include_router(auth_router)

if __name__ == '__main__':
    app.run(debug=True, port=8000)