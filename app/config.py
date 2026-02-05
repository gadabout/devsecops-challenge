from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings are read from the environment, falling back to these defaults."""

    database_url: str = "postgresql://peek:hunter2@localhost:5432/bookings"
    jwt_secret: str = "dev-secret-change-me"
    token_ttl_minutes: int = 60
    debug: bool = True


settings = Settings()
