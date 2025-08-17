from fastapi import APIRouter, Header, HTTPException, Request
from svix import Webhook
from ..config import settings

router = APIRouter(tags=["webhooks"])

@router.post("/clerk")
async def clerk_webhook(request: Request, svix_id: str | None = Header(None, alias="svix-id"), svix_timestamp: str | None = Header(None, alias="svix-timestamp"), svix_signature: str | None = Header(None, alias="svix-signature")):
    if not (svix_id and svix_timestamp and svix_signature):
        raise HTTPException(status_code=400, detail="Missing Svix headers")
    payload = await request.body()
    try:
        wh = Webhook(settings.CLERK_WEBHOOK_SECRET)
        event = wh.verify(payload, {
            "svix-id": svix_id,
            "svix-timestamp": svix_timestamp,
            "svix-signature": svix_signature,
        })
        event_type = event.get("type") if isinstance(event, dict) else getattr(event, "type", None)
        return {"status": "ok", "type": event_type}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

