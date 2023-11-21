from typing import Dict
from bson import ObjectId
from fastapi import BackgroundTasks, Depends, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.background_tasks import update_last_login
from src.auth.schemas import TokenType
from src.auth.utils import decode_jwt, create_jwt_token, verify_password
from src.core.databases.mongo_db import users_collection
from src.core.exceptions import CustomHTTPException


jwt_router = APIRouter(
    prefix="/token",
    tags=["token"],
)


@jwt_router.post('/pair', summary="Create access and refresh tokens for a user", response_model=Dict[str, str])
async def login(background_tasks: BackgroundTasks, form_data: OAuth2PasswordRequestForm = Depends()):
    # In this jwt_router we use email as username
    email = form_data.username
    raw_password = form_data.password
    user_data = await users_collection.find_one({"email": email})
    if not user_data.get('is_active', False):
        raise CustomHTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is inactive"
        )
    # Check that the user with given email exists
    if user_data is None:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    # Check that the specified password is valid for the user
    hashed_password = user_data.get('hashed_password')
    if not verify_password(raw_password, hashed_password):
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    # Update user's last_login field
    query = {"_id": ObjectId(user_data.get("_id"))}
    background_tasks.add_task(update_last_login, query)

    token_pair = {
        "access_token": create_jwt_token(email, TokenType.access),
        "refresh_token": create_jwt_token(email, TokenType.refresh),
    }
    return token_pair


@jwt_router.post("/refresh", response_description="Refresh a token", response_model=Dict[str, str])
async def refresh_token(refresh_token: str):
    payload = decode_jwt(refresh_token)
    if payload is None:
        raise CustomHTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generate a new access token using the same subject
    email = payload.get("sub")
    access_token = create_jwt_token(email, TokenType.access)
    response = {"access_token": access_token}
    return response
