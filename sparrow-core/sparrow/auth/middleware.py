"""Authentication middleware for FastAPI."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from jose import JWTError, jwt

from sparrow.auth.models import Role, TokenPayload, User
from sparrow.config import load_config

security = HTTPBearer(auto_error=False)


def create_access_token(user_id: str, role: Role, expires_hours: int = 24) -> str:
    """Create a JWT access token."""
    config = load_config()
    payload = {
        "sub": user_id,
        "role": role.value,
        "exp": datetime.utcnow() + timedelta(hours=expires_hours),
    }
    return jwt.encode(payload, config.secret_key, algorithm="HS256")


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
) -> User:
    """Extract and validate the current user from JWT token."""
    config = load_config()

    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(credentials.credentials, config.secret_key, algorithms=["HS256"])
        token_data = TokenPayload(
            sub=payload["sub"],
            role=Role(payload["role"]),
            exp=datetime.fromtimestamp(payload["exp"]),
        )
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return User(id=token_data.sub, username=token_data.sub, role=token_data.role)
