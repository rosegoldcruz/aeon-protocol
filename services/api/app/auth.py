from fastapi import Depends, HTTPException, status, Request
from jose import jwt
import requests, time
from .config import settings

class JWKSCache:
    def __init__(self, url: str, ttl_sec: int = 300):
        self.url = url
        self.ttl = ttl_sec
        self.cached = None
        self.exp = 0

    def get(self):
        now = int(time.time())
        if not self.cached or now >= self.exp:
            r = requests.get(self.url, timeout=5)
            r.raise_for_status()
            self.cached = r.json()
            self.exp = now + self.ttl
        return self.cached

_jwks = JWKSCache(settings.CLERK_JWKS_URL)

def verify_bearer(request: Request):
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = auth.split(" ",1)[1]
    try:
        unverified = jwt.get_unverified_header(token)
        jwks = _jwks.get()
        key = next((k for k in jwks.get("keys", []) if k.get("kid") == unverified.get("kid")), None)
        if not key:
            raise HTTPException(status_code=401, detail="Invalid token kid")

        claims = jwt.decode(
            token,
            key,
            algorithms=[unverified.get("alg")],
            audience=settings.CLERK_AUDIENCE,
            issuer=settings.CLERK_ISSUER,
            options={"verify_at_hash": False}
        )
        return claims
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
