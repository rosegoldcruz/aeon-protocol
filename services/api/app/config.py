from pydantic_settings import BaseSettings
from pydantic import AnyUrl
import os

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "production")
    API_PREFIX: str = "/v1"

    # Database
    DATABASE_URL: str

    # Redis / Celery
    REDIS_URL: str

    # S3
    S3_BUCKET: str
    S3_REGION: str
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str

    # Clerk / Auth
    CLERK_JWKS_URL: str
    CLERK_ISSUER: str
    CLERK_AUDIENCE: str

    # Observability
    SENTRY_DSN: str | None = None
    PROMETHEUS_ENABLED: bool = True

settings = Settings()

