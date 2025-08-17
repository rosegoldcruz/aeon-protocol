from fastapi import APIRouter, Depends, HTTPException
from ..auth import verify_bearer
from ..celery_client import generate_video_task, get_task_result

router = APIRouter(tags=["media"])

@router.post("/video/generate")
async def video_generate(payload: dict, claims: dict = Depends(verify_bearer)):
    prompt = (payload or {}).get("prompt", "")
    try:
        task = generate_video_task(prompt=prompt, **(payload or {}))
        return {"job_id": task.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/jobs/{job_id}")
async def job_status(job_id: str, claims: dict = Depends(verify_bearer)):
    try:
        return get_task_result(job_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/library")
async def library_list(claims: dict = Depends(verify_bearer)):
    # Minimal stub; worker persists assets to S3
    return {"items": []}


