from fastapi import APIRouter, Depends, Security, status
from typing import Mapping
from fastapi_pagination import Page, Params, paginate
from bson import ObjectId
from src.auth.dependencies import auhorized_user_role, valid_user_id
from src.auth.schemas import Role, UserToCreate, UserToRetrieve, UserToUpdate
from src.auth.utils import get_hashed_password, oauth2_scheme
from src.core.databases.mongo_db import users_collection
from src.core.exceptions import CustomHTTPException


users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users_router.post("/", response_description="Create a user", response_model=UserToRetrieve)
async def create_user(
        user: UserToCreate,
        authorized_user_role: str = Depends(auhorized_user_role),
        token: str = Security(oauth2_scheme),
    ):
    if authorized_user_role != Role.admin:
        raise CustomHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Required admin role")
    user_data = user.dict()
    user_data["hashed_password"] = get_hashed_password(user_data.pop("raw_password"))
    insert_result = await users_collection.insert_one(user_data)
    created_user_data = {**user_data, "_id": insert_result.inserted_id}
    return created_user_data


@users_router.get("/", response_description="List all users", response_model=Page[UserToRetrieve])
async def get_users(params: Params = Depends(), token: str = Security(oauth2_scheme)):
    cursor = users_collection.find()
    users = await cursor.to_list(length=None)
    users_paginated = paginate(users, params)
    return users_paginated


@users_router.get("/{id}", response_description="Get a user by id", response_model=UserToRetrieve)
async def get_user(user: Mapping = Depends(valid_user_id), token: str = Security(oauth2_scheme)):
    return user


@users_router.patch("/{id}", response_description="Partially update a user", response_model=UserToRetrieve)
async def partially_update_user(
        update_data: UserToUpdate,
        found_user: Mapping = Depends(valid_user_id),
        authorized_user_role: str = Depends(auhorized_user_role),
        token: str = Security(oauth2_scheme)
    ):
    if authorized_user_role != Role.admin:
        raise CustomHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Required admin role")
    # Exclude unset values so they would not be set to defaults
    update_data = update_data.dict(exclude_unset=True)
    if 'hashed_password' in update_data:
        raise CustomHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot change password")
    update_result = await users_collection.update_one({"_id": ObjectId(found_user.get('_id'))}, {"$set": update_data})
    if update_result.modified_count != 1:
        raise CustomHTTPException(status_code=500, detail="Error updating a user")
    # Update found user's data with new data to avoid another database request to get a user
    updated_user = {**found_user, **update_data}
    return updated_user


@users_router.put("/{id}", response_description="Update a user", response_model=UserToRetrieve)
async def update_user(
        update_data: UserToUpdate,
        found_user: Mapping = Depends(valid_user_id),
        authorized_user_role: str = Depends(auhorized_user_role),
        token: str = Security(oauth2_scheme),
    ):
    if authorized_user_role != Role.admin:
        raise CustomHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Required admin role")
    update_data = update_data.dict()
    if 'hashed_password' in update_data:
        raise CustomHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot change password")
    update_result = await users_collection.update_one({"_id": ObjectId(found_user.get('_id'))}, {"$set": update_data})
    if update_result.modified_count != 1:
        raise CustomHTTPException(status_code=500, detail="Error updating a user")
    # Update found user's data with new data to avoid another database request to get a user
    updated_user = {**found_user, **update_data}
    return updated_user


@users_router.delete("/{id}", response_description="Delete a user", response_model=UserToRetrieve)
async def delete_user(
        found_user: Mapping = Depends(valid_user_id),
        authorized_user_role: str = Depends(auhorized_user_role),
        token: str = Security(oauth2_scheme),
    ):
    if authorized_user_role != Role.admin:
        raise CustomHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Required admin role")
    delete_result = await users_collection.delete_one({"_id": ObjectId(found_user.get('_id'))})
    if delete_result.deleted_count == 0:
        raise CustomHTTPException(status_code=500, detail="Error deleting a user")
    return found_user
