from fastapi import Depends, Request, status
from bson.errors import InvalidId
from typing import Mapping
from bson import ObjectId
from src.auth.schemas import Role
from src.core.databases.mongo_db import users_collection
from src.core.exceptions import CustomHTTPException



def valid_objectid(id: str) -> ObjectId:
    try:
        objectid = ObjectId(id)
    except InvalidId as e:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid id"
        )
    return objectid


async def valid_user_id(id: ObjectId = Depends(valid_objectid)) -> Mapping:
    user = await users_collection.find_one({"_id": ObjectId(id)})
    if not user:
        raise CustomHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    return user


async def auhorized_user_role(request: Request) -> Role:
    email = getattr(request.state, 'email', None)
    if email:
        user = await users_collection.find_one({"email": email})
    if not email or not user:
        return None
    role = user.get("role")
    return role