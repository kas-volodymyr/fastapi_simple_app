from motor.motor_asyncio import AsyncIOMotorClient
from src.config import DB_NAME, MONGODB_URL, USERS_COLLECTION_NAME


mongo_client = AsyncIOMotorClient(MONGODB_URL)
mongo_db = mongo_client[DB_NAME]

users_collection = mongo_db.get_collection(USERS_COLLECTION_NAME)

# Define a unique index on the email field
users_collection.create_index("email", unique=True)