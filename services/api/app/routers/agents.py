"""
AI Agent Ecosystem API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..database import get_db, Job, Agent, JobStatus, JobType
from ..auth import get_current_user, AuthenticatedUser
from ..agents.content_agents import ContentAgentFactory, ContentAgentType
from ..agents.business_agents import BusinessAgentFactory, BusinessAgentType
from ..schemas import JobResponse, AgentResponse, AgentTaskInput

router = APIRouter(prefix="/v1/agents", tags=["AI Agents"])

# Content Creation Agents
@router.post("/content/screenwriter", response_model=JobResponse)
async def run_screenwriter_agent(
    task_input: AgentTaskInput,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Run Screenwriter Agent for script generation and story analysis"""
    try:
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "agent_type": "screenwriter",
                "task": task_input.task,
                "parameters": task_input.parameters
            },
            provider="openai"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_screenwriter_task, job.id, task_input.dict())
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run screenwriter agent: {str(e)}")

@router.post("/content/video-editor", response_model=JobResponse)
async def run_video_editor_agent(
    task_input: AgentTaskInput,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Run Video Editor Agent for automated editing and pacing optimization"""
    try:
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "agent_type": "video_editor",
                "task": task_input.task,
                "parameters": task_input.parameters
            },
            provider="openai"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_video_editor_task, job.id, task_input.dict())
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run video editor agent: {str(e)}")

@router.post("/content/seo-optimizer", response_model=JobResponse)
async def run_seo_optimizer_agent(
    task_input: AgentTaskInput,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Run SEO Content Agent for automated content optimization"""
    try:
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "agent_type": "seo_content",
                "task": task_input.task,
                "parameters": task_input.parameters
            },
            provider="openai"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_seo_optimizer_task, job.id, task_input.dict())
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run SEO optimizer agent: {str(e)}")

# Business Automation Agents
@router.post("/business/sales", response_model=JobResponse)
async def run_sales_agent(
    task_input: AgentTaskInput,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Run Sales Agent for lead qualification and proposal generation"""
    try:
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "agent_type": "sales",
                "task": task_input.task,
                "parameters": task_input.parameters
            },
            provider="openai"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_sales_agent_task, job.id, task_input.dict())
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run sales agent: {str(e)}")

@router.post("/business/marketing", response_model=JobResponse)
async def run_marketing_agent(
    task_input: AgentTaskInput,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Run Marketing Agent for campaign creation and optimization"""
    try:
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "agent_type": "marketing",
                "task": task_input.task,
                "parameters": task_input.parameters
            },
            provider="openai"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_marketing_agent_task, job.id, task_input.dict())
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run marketing agent: {str(e)}")

@router.post("/business/customer-service", response_model=JobResponse)
async def run_customer_service_agent(
    task_input: AgentTaskInput,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Run Customer Service Agent for automated support"""
    try:
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "agent_type": "customer_service",
                "task": task_input.task,
                "parameters": task_input.parameters
            },
            provider="openai"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_customer_service_task, job.id, task_input.dict())
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run customer service agent: {str(e)}")

@router.post("/business/analytics", response_model=JobResponse)
async def run_analytics_agent(
    task_input: AgentTaskInput,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Run Analytics Agent for cross-platform data analysis"""
    try:
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "agent_type": "analytics",
                "task": task_input.task,
                "parameters": task_input.parameters
            },
            provider="openai"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_analytics_agent_task, job.id, task_input.dict())
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run analytics agent: {str(e)}")

# Revolutionary Multi-Scene Video Generation Endpoint
@router.post("/content/multi-scene-video", response_model=JobResponse)
async def generate_multi_scene_video(
    task_input: AgentTaskInput,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Revolutionary multi-scene video generation using Screenwriter + Video Editor agents"""
    try:
        from ..agents.orchestration import aeon_orchestrator

        # Create job for the multi-scene video workflow
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "workflow_type": "multi_scene_video_production",
                "concept": task_input.parameters.get("concept", ""),
                "genre": task_input.parameters.get("genre", "drama"),
                "target_duration": task_input.parameters.get("target_duration", 120),
                "target_audience": task_input.parameters.get("target_audience", "general"),
                "style": task_input.parameters.get("style", "cinematic"),
                "platform": task_input.parameters.get("platform", "youtube"),
                "video_provider": task_input.parameters.get("video_provider", "runway"),
                "voice_id": task_input.parameters.get("voice_id", "21m00Tcm4TlvDq8ikWAM")
            },
            provider="aeon_orchestrator"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        # Execute the revolutionary workflow in background
        background_tasks.add_task(
            process_multi_scene_video_workflow,
            job.id,
            task_input.parameters
        )

        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start multi-scene video generation: {str(e)}")

# Agent Orchestration Endpoints
@router.post("/orchestration/execute-workflow", response_model=JobResponse)
async def execute_agent_workflow(
    workflow_name: str,
    input_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Execute a predefined agent workflow"""
    try:
        from ..agents.orchestration import aeon_orchestrator

        # Validate workflow exists
        available_workflows = aeon_orchestrator.get_available_workflows()
        if workflow_name not in available_workflows:
            raise HTTPException(status_code=400, detail=f"Unknown workflow: {workflow_name}")

        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "workflow_name": workflow_name,
                "input_data": input_data
            },
            provider="aeon_orchestrator"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)

        background_tasks.add_task(
            process_agent_workflow,
            job.id,
            workflow_name,
            input_data
        )

        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute workflow: {str(e)}")

@router.get("/orchestration/workflows")
async def get_available_workflows():
    """Get list of available agent workflows"""
    try:
        from ..agents.orchestration import aeon_orchestrator
        return {
            "workflows": aeon_orchestrator.get_available_workflows(),
            "agents": aeon_orchestrator.get_agent_capabilities()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get workflows: {str(e)}")

# Background processing functions
async def process_multi_scene_video_workflow(job_id: int, parameters: Dict[str, Any]):
    """Process the revolutionary multi-scene video generation workflow"""
    try:
        from ..agents.orchestration import aeon_orchestrator
        from ..celery_client import celery_app

        # Execute the Screenwriter → Video Editor workflow
        workflow_input = {
            "concept": parameters.get("concept", ""),
            "genre": parameters.get("genre", "drama"),
            "target_duration": parameters.get("target_duration", 120),
            "target_audience": parameters.get("target_audience", "general"),
            "style": parameters.get("style", "cinematic"),
            "platform": parameters.get("platform", "youtube"),
            "video_provider": parameters.get("video_provider", "runway"),
            "voice_id": parameters.get("voice_id", "21m00Tcm4TlvDq8ikWAM")
        }

        # Execute the workflow
        results = await aeon_orchestrator.execute_workflow("multi_scene_video_production", workflow_input)

        # If we have scenes from screenwriter, trigger multi-scene video generation
        if len(results) >= 2 and results[1].success:
            video_editor_output = results[1].data
            if "execution_plan" in video_editor_output:
                execution_plan = video_editor_output["execution_plan"]

                # Send to worker for actual video generation and stitching
                celery_task = celery_app.send_task(
                    "worker.generate_multi_scene_video",
                    args=[execution_plan["scenes"]],
                    kwargs={
                        "job_id": job_id,
                        "video_provider": execution_plan["video_provider"],
                        "voice_id": execution_plan["voice_id"],
                        "platform": execution_plan["platform"]
                    }
                )

                # Update job with celery task ID
                # This would need database access in real implementation

        # Update job status
        # This would need database access in real implementation

    except Exception as e:
        # Handle errors
        # This would need database access in real implementation
        pass

async def process_agent_workflow(job_id: int, workflow_name: str, input_data: Dict[str, Any]):
    """Process a general agent workflow"""
    try:
        from ..agents.orchestration import aeon_orchestrator

        # Execute the workflow
        results = await aeon_orchestrator.execute_workflow(workflow_name, input_data)

        # Update job with results
        # This would need database access in real implementation

    except Exception as e:
        # Handle errors
        # This would need database access in real implementation
        pass

# Agent Management
@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all available AI agents"""
    try:
        result = await db.execute(
            select(Agent).where(
                Agent.tenant_id == current_user.tenant_id,
                Agent.is_active == True
            )
        )
        agents = result.scalars().all()
        
        return [
            AgentResponse(
                id=agent.id,
                name=agent.name,
                type=agent.type,
                description=agent.description,
                configuration=agent.configuration,
                is_active=agent.is_active,
                created_at=agent.created_at
            )
            for agent in agents
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list agents: {str(e)}")

# Background processing functions
async def process_screenwriter_task(job_id: int, task_data: Dict[str, Any]):
    """Process screenwriter agent task"""
    pass

async def process_video_editor_task(job_id: int, task_data: Dict[str, Any]):
    """Process video editor agent task"""
    pass

async def process_seo_optimizer_task(job_id: int, task_data: Dict[str, Any]):
    """Process SEO optimizer agent task"""
    pass

async def process_sales_agent_task(job_id: int, task_data: Dict[str, Any]):
    """Process sales agent task"""
    pass

async def process_marketing_agent_task(job_id: int, task_data: Dict[str, Any]):
    """Process marketing agent task"""
    pass

async def process_customer_service_task(job_id: int, task_data: Dict[str, Any]):
    """Process customer service agent task"""
    pass

async def process_analytics_agent_task(job_id: int, task_data: Dict[str, Any]):
    """Process analytics agent task"""
    pass
