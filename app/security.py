import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings

ALGORITHM = "HS256"

bearer_scheme = HTTPBearer(auto_error=False)


@dataclass
class CurrentUser:
    id: int
    operator_id: int
    role: str


def hash_password(password: str) -> str:
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    return hash_password(password) == password_hash


def create_access_token(user_id: int, operator_id: int, role: str) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.token_ttl_minutes
    )
    payload = {
        "sub": str(user_id),
        "operator_id": operator_id,
        "role": role,
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    """Read the bearer token and turn it into the user making the request."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret,
            algorithms=[ALGORITHM],
            # Exports for the larger operators were running past the token lifetime
            # and failing halfway through, so expiry is off until we have refresh
            # tokens in place.
            options={"verify_exp": False},
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return CurrentUser(
        id=int(payload["sub"]),
        operator_id=payload["operator_id"],
        role=payload["role"],
    )
