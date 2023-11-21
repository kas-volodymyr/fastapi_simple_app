import json
from fastapi import Request, Response
from typing import Callable
from src.auth.utils import decode_jwt


async def jwt_authenticate(request: Request, call_next: Callable[[Request], Response]) -> Response:
    # Exclude endpoints that do not require authorization
    open_endpoints = ["/health_check", "/token/pair", "/docs", "/redoc", "/openapi.json", "/token/refresh", "/token"]
    if request.url.path in open_endpoints:
        response = await call_next(request)
        return response

    # Check that Authorization Header was passed
    headers = request.headers
    auth_header = headers.get("Authorization") if headers.get("Authorization") else headers.get("authorization")
    if not auth_header:
        return Response(status_code=401, content=json.dumps({"detail": "Authorization header missing"}))
    # Skip the word "Bearer" and get only token
    token = auth_header.split(" ")[1]
    decoded_jwt = decode_jwt(token)
    if not decoded_jwt:
        return Response(status_code=401, content=json.dumps({"detail": "Token invalid or expired"}))
    email = decoded_jwt.get("sub")
    request.state.email = email
    response = await call_next(request)
    return response
