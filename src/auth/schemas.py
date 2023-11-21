from datetime import datetime
import re
from bson import ObjectId
from pydantic import Field, validator, BaseModel
from typing import Optional
from enum import Enum
from pydantic import EmailStr


class Role(str, Enum):
    admin = "admin"
    developer = "developer"
    simple_mortal = "simple mortal"


class TokenType(str, Enum):
    access = 'access'
    refresh = 'refresh'


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=128)
    last_name: str = Field(min_length=1, max_length=128)
    role: Role
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None


class UserToCreate(UserBase):
    raw_password: str
    is_active: bool = True
    created_at: datetime = datetime.now()

    @validator('raw_password')
    def raw_password_strength(cls, password: str) -> str:
        errors = []
        if len(password) < 8:
            errors.append('Password length should be at least 8 symbols')
        if not any(char.isdigit() for char in password):
            errors.append('Password should contain at least one digit')
        if not re.search("[a-z]", password):
            errors.append('Password must contain at least 1 lowercase letter')
        if not re.search("[A-Z]", password):
            errors.append('Password must contain at least 1 uppercase letter')
        if not re.search("[^a-zA-Z0-9]", password):
            errors.append('Password must contain at least 1 special symbol')
        if errors:
            raise ValueError(errors)
        return password


class UserToRetrieve(UserBase):
    id: PyObjectId = Field(default_factory = PyObjectId, alias = "_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserToUpdate(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str] = Field(min_length=1, max_length=128)
    last_name: Optional[str] = Field(min_length=1, max_length=128)
    role: Optional[Role]
    is_active: Optional[bool]
