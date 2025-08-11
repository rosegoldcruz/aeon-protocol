"""
Workflow Automation API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..database import get_db, Workflow, Job, JobStatus, JobType
from ..auth import get_current_user, AuthenticatedUser
from ..schemas import WorkflowResponse, WorkflowCreateInput, JobResponse

router = APIRouter(prefix="/v1/workflows", tags=["Workflow Automation"])

@router.post("/", response_model=WorkflowResponse)
async def create_workflow(
    workflow_data: WorkflowCreateInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new workflow automation"""
    try:
        workflow = Workflow(
            tenant_id=current_user.tenant_id,
            name=workflow_data.name,
            description=workflow_data.description,
            definition=workflow_data.definition,
            is_active=workflow_data.is_active,
            created_by=current_user.user_id
        )
        db.add(workflow)
        await db.commit()
        await db.refresh(workflow)
        
        return WorkflowResponse(
            id=workflow.id,
            name=workflow.name,
            description=workflow.description,
            definition=workflow.definition,
            is_active=workflow.is_active,
            trigger_count=workflow.trigger_count,
            success_count=workflow.success_count,
            error_count=workflow.error_count,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create workflow: {str(e)}")

@router.get("/", response_model=List[WorkflowResponse])
async def list_workflows(
    is_active: Optional[bool] = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all workflows for the tenant"""
    try:
        query = select(Workflow).where(Workflow.tenant_id == current_user.tenant_id)
        
        if is_active is not None:
            query = query.where(Workflow.is_active == is_active)
        
        result = await db.execute(query)
        workflows = result.scalars().all()
        
        return [
            WorkflowResponse(
                id=workflow.id,
                name=workflow.name,
                description=workflow.description,
                definition=workflow.definition,
                is_active=workflow.is_active,
                trigger_count=workflow.trigger_count,
                success_count=workflow.success_count,
                error_count=workflow.error_count,
                created_at=workflow.created_at,
                updated_at=workflow.updated_at
            )
            for workflow in workflows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list workflows: {str(e)}")

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: int,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get workflow by ID"""
    try:
        result = await db.execute(
            select(Workflow).where(
                Workflow.id == workflow_id,
                Workflow.tenant_id == current_user.tenant_id
            )
        )
        workflow = result.scalar_one_or_none()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        return WorkflowResponse(
            id=workflow.id,
            name=workflow.name,
            description=workflow.description,
            definition=workflow.definition,
            is_active=workflow.is_active,
            trigger_count=workflow.trigger_count,
            success_count=workflow.success_count,
            error_count=workflow.error_count,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get workflow: {str(e)}")

@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int,
    workflow_data: WorkflowCreateInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update workflow"""
    try:
        result = await db.execute(
            select(Workflow).where(
                Workflow.id == workflow_id,
                Workflow.tenant_id == current_user.tenant_id
            )
        )
        workflow = result.scalar_one_or_none()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        workflow.name = workflow_data.name
        workflow.description = workflow_data.description
        workflow.definition = workflow_data.definition
        workflow.is_active = workflow_data.is_active
        workflow.updated_at = datetime.now()
        
        await db.commit()
        await db.refresh(workflow)
        
        return WorkflowResponse(
            id=workflow.id,
            name=workflow.name,
            description=workflow.description,
            definition=workflow.definition,
            is_active=workflow.is_active,
            trigger_count=workflow.trigger_count,
            success_count=workflow.success_count,
            error_count=workflow.error_count,
            created_at=workflow.created_at,
            updated_at=workflow.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update workflow: {str(e)}")

@router.post("/{workflow_id}/trigger", response_model=JobResponse)
async def trigger_workflow(
    workflow_id: int,
    trigger_data: Dict[str, Any],
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Manually trigger a workflow"""
    try:
        result = await db.execute(
            select(Workflow).where(
                Workflow.id == workflow_id,
                Workflow.tenant_id == current_user.tenant_id,
                Workflow.is_active == True
            )
        )
        workflow = result.scalar_one_or_none()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Active workflow not found")
        
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "workflow_id": workflow_id,
                "trigger_data": trigger_data,
                "workflow_definition": workflow.definition
            },
            provider="workflow_engine"
        )
        db.add(job)
        
        # Update workflow trigger count
        workflow.trigger_count += 1
        
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_workflow_execution, job.id, workflow_id, trigger_data)
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger workflow: {str(e)}")

@router.delete("/{workflow_id}")
async def delete_workflow(
    workflow_id: int,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete workflow"""
    try:
        result = await db.execute(
            select(Workflow).where(
                Workflow.id == workflow_id,
                Workflow.tenant_id == current_user.tenant_id
            )
        )
        workflow = result.scalar_one_or_none()
        
        if not workflow:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        await db.delete(workflow)
        await db.commit()
        
        return {"message": "Workflow deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete workflow: {str(e)}")

# Background processing functions
async def process_workflow_execution(job_id: int, workflow_id: int, trigger_data: Dict[str, Any]):
    """Process workflow execution in background"""
    try:
        from ..agents.orchestration import aeon_orchestrator
        from ..database.neon_db import get_db

        # Get workflow definition from database
        async with get_db() as db:
            result = await db.execute(
                select(Workflow).where(Workflow.id == workflow_id)
            )
            workflow = result.scalar_one_or_none()

            if not workflow:
                raise Exception(f"Workflow {workflow_id} not found")

            workflow_definition = workflow.definition

            # Check if this is a predefined workflow
            if "workflow_type" in workflow_definition:
                workflow_type = workflow_definition["workflow_type"]

                # Execute predefined workflow
                if workflow_type in aeon_orchestrator.workflows:
                    results = await aeon_orchestrator.execute_workflow(workflow_type, trigger_data)
                else:
                    # Execute custom workflow
                    agent_types = workflow_definition.get("agents", [])
                    input_mappings = workflow_definition.get("input_mappings", [])
                    results = await aeon_orchestrator.execute_custom_chain(
                        agent_types, trigger_data, input_mappings
                    )
            else:
                # Legacy workflow format - execute as custom chain
                agent_types = workflow_definition.get("steps", [])
                results = await aeon_orchestrator.execute_custom_chain(agent_types, trigger_data)

            # Update job with results
            job = await db.get(Job, job_id)
            if job:
                job.status = JobStatus.COMPLETED
                job.output_data = {
                    "workflow_results": [result.to_dict() for result in results],
                    "execution_summary": {
                        "total_steps": len(results),
                        "successful_steps": sum(1 for r in results if r.success),
                        "failed_steps": sum(1 for r in results if not r.success),
                        "workflow_id": workflow_id
                    }
                }

                # Update workflow statistics
                workflow.trigger_count += 1
                if all(result.success for result in results):
                    workflow.success_count += 1
                else:
                    workflow.error_count += 1

                await db.commit()

    except Exception as e:
        # Update job with error
        async with get_db() as db:
            job = await db.get(Job, job_id)
            if job:
                job.status = JobStatus.FAILED
                job.error_message = str(e)
                await db.commit()
