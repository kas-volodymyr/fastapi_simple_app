from datetime import datetime
from src.core.databases.mongo_db import users_collection


async def update_last_login(query: dict):
    update_data = {'last_login': datetime.now()}
    await users_collection.update_one(query, {"$set": update_data})
    