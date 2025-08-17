from pydantic_settings import BaseSettings

class Settings(BaseSettings):
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
    CLERK_WEBHOOK_SECRET: str

    # Observability & CORS
    PROMETHEUS_ENABLED: bool
    CORS_ALLOW_ORIGINS: str

settings = Settings()

