from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class BookingRequest(BaseModel):
    activity_id: int
    customer_name: str = Field(min_length=1, max_length=120)
    customer_email: EmailStr
    customer_phone: str | None = Field(default=None, max_length=32)
    party_size: int = Field(ge=1, le=20)


class WebhookRequest(BaseModel):
    url: str
