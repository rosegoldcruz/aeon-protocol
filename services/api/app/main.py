from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime

from .database import get_db
from .models import Job, Asset, Tenant, User, Project, JobStatus, JobType
from .schemas import (
    JobCreate, JobResponse, JobListResponse, ImageGenerationInput,
    AssetResponse, ErrorResponse, VideoGenerationInput, AudioGenerationInput
)
from .celery_client import generate_image_task, generate_video_task, generate_audio_task, get_task_result
from .s3_client import generate_presigned_url
from .auth import get_current_user, AuthenticatedUser, require_editor

app = FastAPI(title="AEON API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://poetic-bluebird-21.clerk.accounts.dev",
        "https://api.clerk.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/v1/jobs/image-generate", response_model=JobResponse)
async def create_image_generation_job(
    input_data: ImageGenerationInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new image generation job"""
    try:
        # Create job record
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.IMAGE_GENERATION,
            status=JobStatus.PENDING,
            input_data=input_data.dict(),
            provider="replicate"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        # Send task to worker
        task = generate_image_task(
            prompt=input_data.prompt,
            job_id=job.id,
            model=input_data.model,
            width=input_data.width,
            height=input_data.height,
            num_outputs=input_data.num_outputs,
            guidance_scale=input_data.guidance_scale,
            num_inference_steps=input_data.num_inference_steps
        )

        # Update job with provider task ID
        job.provider_job_id = task.id
        job.status = JobStatus.PROCESSING
        await db.commit()
        await db.refresh(job)

        return job

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/jobs/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get job by ID"""
    result = await db.execute(
        select(Job).where(Job.id == job_id, Job.tenant_id == current_user.tenant_id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check task status if still processing
    if job.status == JobStatus.PROCESSING and job.provider_job_id:
        task_result = get_task_result(job.provider_job_id)

        if task_result["status"] == "SUCCESS":
            job.status = JobStatus.COMPLETED
            job.output_data = task_result["result"]
            job.completed_at = datetime.now()
            await db.commit()
        elif task_result["status"] == "FAILURE":
            job.status = JobStatus.FAILED
            job.error_message = str(task_result["result"])
            await db.commit()

    return job

@app.get("/v1/jobs", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: Optional[JobStatus] = None,
    type: Optional[JobType] = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List jobs with pagination"""
    query = select(Job).where(Job.tenant_id == current_user.tenant_id)

    if status:
        query = query.where(Job.status == status)
    if type:
        query = query.where(Job.type == type)

    # Get total count
    count_query = select(func.count(Job.id)).where(Job.tenant_id == current_user.tenant_id)
    if status:
        count_query = count_query.where(Job.status == status)
    if type:
        count_query = count_query.where(Job.type == type)

    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Get paginated results
    query = query.order_by(Job.created_at.desc())
    query = query.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(query)
    jobs = result.scalars().all()

    return JobListResponse(
        jobs=jobs,
        total=total,
        page=page,
        per_page=per_page
    )

@app.get("/v1/jobs/{job_id}/assets", response_model=List[AssetResponse])
async def get_job_assets(
    job_id: int,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get assets for a job"""
    # Verify job exists and belongs to tenant
    job_result = await db.execute(
        select(Job).where(Job.id == job_id, Job.tenant_id == current_user.tenant_id)
    )
    job = job_result.scalar_one_or_none()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Get assets
    result = await db.execute(
        select(Asset).where(Asset.job_id == job_id)
    )
    assets = result.scalars().all()

    # Add presigned URLs
    for asset in assets:
        asset.presigned_url = generate_presigned_url(asset.s3_key, asset.s3_bucket)

    return assets

@app.post("/v1/jobs/video-generate", response_model=JobResponse)
async def create_video_generation_job(
    input_data: VideoGenerationInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new video generation job"""
    try:
        # Create job record
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.VIDEO_GENERATION,
            status=JobStatus.PENDING,
            input_data=input_data.dict(),
            provider=input_data.provider
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        # Send task to worker
        task = generate_video_task(
            prompt=input_data.prompt,
            job_id=job.id,
            provider=input_data.provider,
            video_type=input_data.video_type,
            image_url=input_data.image_url,
            duration=input_data.duration,
            resolution=input_data.resolution,
            aspect_ratio=input_data.aspect_ratio,
            motion_strength=input_data.motion_strength,
            fps=input_data.fps,
            guidance_scale=input_data.guidance_scale,
            negative_prompt=input_data.negative_prompt
        )

        # Update job with provider task ID
        job.provider_job_id = task.id
        job.status = JobStatus.PROCESSING
        await db.commit()
        await db.refresh(job)

        return job

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/jobs/audio-generate", response_model=JobResponse)
async def create_audio_generation_job(
    input_data: AudioGenerationInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new audio generation job"""
    try:
        # Create job record
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AUDIO_GENERATION,
            status=JobStatus.PENDING,
            input_data=input_data.dict(),
            provider="elevenlabs"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        # Send task to worker
        task = generate_audio_task(
            text=input_data.text,
            job_id=job.id,
            voice_id=input_data.voice_id,
            model_id=input_data.model_id,
            stability=input_data.stability,
            similarity_boost=input_data.similarity_boost
        )

        # Update job with provider task ID
        job.provider_job_id = task.id
        job.status = JobStatus.PROCESSING
        await db.commit()
        await db.refresh(job)

        return job

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# AI Agents endpoints
@app.post("/v1/agents/content/{agent_type}")
async def run_content_agent(
    agent_type: str,
    input_data: Dict[str, Any],
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Run content creation agents"""
    try:
        from .agents.content_agents import ScreenwriterAgent, VideoEditorAgent, ContentOptimizerAgent, SEOContentAgent

        # Map agent types to classes
        agent_map = {
            "screenwriter": ScreenwriterAgent,
            "video_editor": VideoEditorAgent,
            "content_optimizer": ContentOptimizerAgent,
            "seo_content": SEOContentAgent
        }

        if agent_type not in agent_map:
            raise HTTPException(status_code=400, detail=f"Unknown agent type: {agent_type}")

        # Create and run agent
        agent = agent_map[agent_type]()
        result = agent.process(input_data)

        # Create job record for tracking
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.IMAGE_GENERATION,  # We'll add AGENT_TASK type later
            status=JobStatus.COMPLETED,
            input_data=input_data,
            output_data=result,
            provider=f"agent_{agent_type}"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        return {
            "job_id": job.id,
            "agent_type": agent_type,
            "result": result,
            "status": "completed"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/agents/business/{agent_type}")
async def run_business_agent(
    agent_type: str,
    input_data: Dict[str, Any],
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Run business automation agents"""
    try:
        from .agents.business_agents import SalesAgent, CustomerServiceAgent, MarketingAgent, AnalyticsAgent

        # Map agent types to classes
        agent_map = {
            "sales": SalesAgent,
            "customer_service": CustomerServiceAgent,
            "marketing": MarketingAgent,
            "analytics": AnalyticsAgent
        }

        if agent_type not in agent_map:
            raise HTTPException(status_code=400, detail=f"Unknown agent type: {agent_type}")

        # Create and run agent
        agent = agent_map[agent_type]()
        result = agent.process(input_data)

        # Create job record for tracking
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.IMAGE_GENERATION,  # We'll add AGENT_TASK type later
            status=JobStatus.COMPLETED,
            input_data=input_data,
            output_data=result,
            provider=f"agent_{agent_type}"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        return {
            "job_id": job.id,
            "agent_type": agent_type,
            "result": result,
            "status": "completed"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

