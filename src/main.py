
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.base import BaseHTTPMiddleware
from src.auth.middlewares import jwt_authenticate
from src.auth.routers.users_router import users_router
from src.auth.routers.jwt_router import jwt_router
from src.core.exceptions import CustomHTTPException, http_exception_handler
from src.journal_management.journal_router import journal_router

app = FastAPI()

app.add_middleware(BaseHTTPMiddleware, dispatch=jwt_authenticate)
app.add_exception_handler(CustomHTTPException, http_exception_handler)

add_pagination(app)

app.include_router(users_router)
app.include_router(jwt_router)
app.include_router(journal_router)

@app.get("/health_check")
async def health_check():
    return {"message": "All good!"}