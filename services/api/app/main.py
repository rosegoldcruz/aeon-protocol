from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import os
from .config import settings
from .routers import media  # keep others disabled until compile passes cleanly

app = FastAPI(title="AEON API")

# CORS: set from env
ALLOWED_ORIGINS = os.getenv("CORS_ALLOW_ORIGINS","https://aeonprotocol.com,https://app.aeonprotocol.com,https://api.aeonprotocol.com,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

REQS = Counter("requests_total","Total HTTP requests")
@app.middleware("http")
async def count_requests(request, call_next):
    REQS.inc()
    return await call_next(request)

@app.get("/metrics")
def metrics():
    if not settings.PROMETHEUS_ENABLED:
        return Response(status_code=404)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(media.router, prefix=settings.API_PREFIX)

