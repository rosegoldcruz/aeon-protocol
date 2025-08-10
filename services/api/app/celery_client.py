import os
from celery import Celery

# Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Create Celery client to send tasks to worker
celery_app = Celery(
    "aeon_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=[]
)

# Task signatures - these match the tasks defined in the worker
def generate_image_task(prompt: str, **kwargs):
    """Send image generation task to worker"""
    return celery_app.send_task(
        "worker.generate_image",
        args=[prompt],
        kwargs=kwargs
    )

def generate_video_task(prompt: str, **kwargs):
    """Send video generation task to worker"""
    return celery_app.send_task(
        "worker.generate_video",
        args=[prompt],
        kwargs=kwargs
    )

def generate_audio_task(text: str, **kwargs):
    """Send audio generation task to worker"""
    return celery_app.send_task(
        "worker.generate_audio",
        args=[text],
        kwargs=kwargs
    )

def get_task_result(task_id: str):
    """Get task result by ID"""
    result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
        "traceback": result.traceback if result.failed() else None
    }
