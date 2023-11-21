import os
import pydantic
from dotenv import load_dotenv
from bson import ObjectId


# Serialize ObjectId from MongoDB to string representation
pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

# Load envorinment variables
load_dotenv()
ENV = os.environ

# Database configs
MONGODB_URL = ENV.get("MONGODB_URL")
DB_NAME = ENV.get("DB_NAME")

# JWT configs
ACCESS_TOKEN_EXPIRE_MINUTES = 20
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
HASHING_ALGORITHM = ENV.get("HASHING_ALGORITHM")
JWT_ACCESS_SECRET_KEY = ENV.get("JWT_ACCESS_SECRET_KEY")
JWT_REFRESH_SECRET_KEY = ENV.get("JWT_REFRESH_SECRET_KEY")

# Collections
USERS_COLLECTION_NAME = ENV.get("USERS_COLLECTION_NAME")