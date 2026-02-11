from fastapi import APIRouter, HTTPException

from app.db import cursor
from app.schemas import LoginRequest, LoginResponse
from app.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest):
    with cursor() as cur:
        cur.execute(
            "SELECT id, operator_id, role, password_hash FROM users WHERE email = %s",
            (body.email,),
        )
        user = cur.fetchone()

    if user is None or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["id"], user["operator_id"], user["role"])
    return LoginResponse(access_token=token)
