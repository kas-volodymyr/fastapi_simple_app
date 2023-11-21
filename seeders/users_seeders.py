from datetime import datetime
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
ENV = os.environ

mongo_client = AsyncIOMotorClient(ENV.get("MONGODB_URL"))
mongo_db = mongo_client['user_db']
users_collection = mongo_db.get_collection(ENV.get("USERS_COLLECTION_NAME"))
users_collection.create_index("email", unique=True)


seed_data = [
    {
        "email": "admin@corporation.com",
        "first_name": "John",
        "last_name": "Dee",
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now(),
        "last_login": None,
        "hashed_password": "$2b$12$tOYlcl1XR4Mh13t2sZvZ2eCEceQEfx.0orLBILXnTr7ZDZvrKEw1G"
    },
    {
        "email": "developer@corporation.com",
        "first_name": "Adam",
        "last_name": "Smith",
        "role": "developer",
        "is_active": True,
        "created_at": datetime.now(),
        "last_login": None,
        "hashed_password": "$2b$12$9nWRdLYpb7HsdO0BNEcUqulPO/9tWTM9KkbP.VJBwqXYqCopWj3xa"
    },
    {
        "email": "simple@corporation.com",
        "first_name": "James",
        "last_name": "Bond",
        "role": "simple mortal",
        "is_active": True,
        "created_at": datetime.now(),
        "last_login": None,
        "hashed_password": "$2b$12$NO5wZ83gakaeV72KDhGpSe61cDrUFTf8RB9ttgHpOFbIB9HuMqSCu"
    },
]

# Insert the seed data into the collection
users_collection.insert_many(seed_data)
print(f"Inserted seeders")