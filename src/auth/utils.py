from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import JWTError, jwt
from src.auth.schemas import TokenType
from src.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES, HASHING_ALGORITHM, JWT_REFRESH_SECRET_KEY,
    JWT_ACCESS_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES
)


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/pair")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_jwt_token(subject: Union[str, Any], token_type: str = TokenType) -> str:
    exp_delta = ACCESS_TOKEN_EXPIRE_MINUTES if token_type == TokenType.access else REFRESH_TOKEN_EXPIRE_MINUTES
    secret = JWT_ACCESS_SECRET_KEY if token_type == TokenType.access else JWT_REFRESH_SECRET_KEY
    expiration_datetime = datetime.utcnow() + timedelta(minutes=exp_delta)
    to_encode = {
        "exp": expiration_datetime,
        "sub": str(subject),
    }
    encoded_jwt = jwt.encode(to_encode, secret, HASHING_ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str, token_type: str = TokenType.access):
    secret = JWT_ACCESS_SECRET_KEY if token_type == TokenType.access else JWT_REFRESH_SECRET_KEY
    try:
        payload = jwt.decode(token, secret, algorithms=[HASHING_ALGORITHM])
        return payload
    except JWTError:
        return None
