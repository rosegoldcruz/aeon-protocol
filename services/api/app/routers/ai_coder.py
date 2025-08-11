"""
AI Coder API endpoints for natural language to web app generation
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List, Optional
import io
import json

from ..database.neon_db import get_db, Job, JobType, JobStatus
from ..auth import get_current_user, AuthenticatedUser
from ..schemas import JobResponse
from ..ai_coder.code_generator import ai_code_generator, GeneratedApp

router = APIRouter(prefix="/ai-coder", tags=["AI Coder"])

# Pydantic models for request/response
from pydantic import BaseModel

class AppGenerationRequest(BaseModel):
    description: str
    app_type: str = "web"
    features: str = ""
    style: str = ""
    framework: str = "react"

class AppGenerationResponse(BaseModel):
    job_id: int
    app_id: str
    status: str
    estimated_time: int

class GeneratedAppResponse(BaseModel):
    app_id: str
    name: str
    description: str
    framework: str
    files: Dict[str, str]
    preview_url: Optional[str] = None
    deployment_url: Optional[str] = None
    metadata: Dict[str, Any]

class DeploymentRequest(BaseModel):
    app_id: str
    platform: str = "vercel"  # vercel, netlify, github-pages
    custom_domain: Optional[str] = None
    environment_variables: Dict[str, str] = {}

@router.post("/generate", response_model=AppGenerationResponse)
async def generate_app(
    request: AppGenerationRequest,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate a web application from natural language description"""
    try:
        # Create job record
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "operation": "ai_coder_generation",
                "description": request.description,
                "app_type": request.app_type,
                "features": request.features,
                "style": request.style,
                "framework": request.framework
            },
            provider="ai_coder"
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        # Start background generation
        background_tasks.add_task(
            process_app_generation,
            job.id,
            request.dict()
        )
        
        return AppGenerationResponse(
            job_id=job.id,
            app_id=f"app_{job.id}",
            status="generating",
            estimated_time=120  # 2 minutes estimated
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start app generation: {str(e)}")

@router.get("/apps/{app_id}", response_model=GeneratedAppResponse)
async def get_generated_app(
    app_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get details of a generated application"""
    try:
        # Extract job ID from app_id (format: app_{job_id})
        job_id = int(app_id.replace("app_", ""))
        
        # Get job from database
        job = await db.get(Job, job_id)
        if not job or job.tenant_id != current_user.tenant_id:
            raise HTTPException(status_code=404, detail="App not found")
        
        if job.status != JobStatus.COMPLETED:
            raise HTTPException(status_code=400, detail=f"App generation status: {job.status}")
        
        if not job.output_data:
            raise HTTPException(status_code=400, detail="App data not available")
        
        app_data = job.output_data
        
        return GeneratedAppResponse(
            app_id=app_id,
            name=app_data.get("name", "Generated App"),
            description=app_data.get("description", ""),
            framework=app_data.get("framework", "react"),
            files=app_data.get("files", {}),
            preview_url=app_data.get("preview_url"),
            deployment_url=app_data.get("deployment_url"),
            metadata=app_data.get("metadata", {})
        )
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid app ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get app: {str(e)}")

@router.post("/apps/{app_id}/preview")
async def create_preview(
    app_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a preview URL for the generated app"""
    try:
        job_id = int(app_id.replace("app_", ""))
        job = await db.get(Job, job_id)
        
        if not job or job.tenant_id != current_user.tenant_id:
            raise HTTPException(status_code=404, detail="App not found")
        
        if job.status != JobStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="App not ready for preview")
        
        # Create preview (would integrate with preview service)
        preview_url = f"https://preview.aeon.ai/apps/{app_id}"
        
        # Update job with preview URL
        if not job.output_data:
            job.output_data = {}
        job.output_data["preview_url"] = preview_url
        await db.commit()
        
        return {"preview_url": preview_url}
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid app ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create preview: {str(e)}")

@router.post("/apps/{app_id}/deploy")
async def deploy_app(
    app_id: str,
    request: DeploymentRequest,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Deploy the generated app to a hosting platform"""
    try:
        job_id = int(app_id.replace("app_", ""))
        job = await db.get(Job, job_id)
        
        if not job or job.tenant_id != current_user.tenant_id:
            raise HTTPException(status_code=404, detail="App not found")
        
        if job.status != JobStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="App not ready for deployment")
        
        # Create deployment job
        deployment_job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "operation": "app_deployment",
                "app_id": app_id,
                "platform": request.platform,
                "custom_domain": request.custom_domain,
                "environment_variables": request.environment_variables,
                "source_job_id": job_id
            },
            provider="deployment_service"
        )
        db.add(deployment_job)
        await db.commit()
        await db.refresh(deployment_job)
        
        # Start background deployment
        background_tasks.add_task(
            process_app_deployment,
            deployment_job.id,
            app_id,
            request.dict()
        )
        
        return {
            "deployment_job_id": deployment_job.id,
            "status": "deploying",
            "estimated_time": 300  # 5 minutes estimated
        }
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid app ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start deployment: {str(e)}")

@router.get("/apps/{app_id}/download")
async def download_app(
    app_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download the generated app as a ZIP file"""
    try:
        job_id = int(app_id.replace("app_", ""))
        job = await db.get(Job, job_id)
        
        if not job or job.tenant_id != current_user.tenant_id:
            raise HTTPException(status_code=404, detail="App not found")
        
        if job.status != JobStatus.COMPLETED or not job.output_data:
            raise HTTPException(status_code=400, detail="App not ready for download")
        
        # Create GeneratedApp object from job data
        app_data = job.output_data
        generated_app = GeneratedApp(
            app_id=app_id,
            name=app_data.get("name", "generated-app"),
            description=app_data.get("description", ""),
            framework=app_data.get("framework", "react"),
            files=app_data.get("files", {}),
            metadata=app_data.get("metadata", {})
        )
        
        # Export as ZIP
        zip_data = ai_code_generator.export_app(generated_app)
        
        return StreamingResponse(
            io.BytesIO(zip_data),
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={generated_app.name}.zip"}
        )
        
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid app ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download app: {str(e)}")

@router.get("/frameworks")
async def get_supported_frameworks():
    """Get list of supported frameworks"""
    return {
        "frameworks": ai_code_generator.supported_frameworks,
        "default": "react",
        "recommended": ["react", "next", "vue"]
    }

@router.get("/examples")
async def get_app_examples():
    """Get example app descriptions for inspiration"""
    return {
        "examples": [
            {
                "name": "Task Management App",
                "description": "A simple todo app with drag-and-drop functionality, categories, and due dates",
                "features": "Add/edit/delete tasks, drag and drop, categories, due dates, search",
                "style": "Clean, modern interface with dark mode support"
            },
            {
                "name": "Weather Dashboard",
                "description": "Weather app showing current conditions and 7-day forecast with location search",
                "features": "Current weather, 7-day forecast, location search, weather maps, alerts",
                "style": "Colorful, visual design with weather-themed animations"
            },
            {
                "name": "Recipe Finder",
                "description": "Recipe search app with ingredient-based filtering and cooking instructions",
                "features": "Recipe search, ingredient filters, cooking timer, favorites, shopping list",
                "style": "Food-focused design with appetizing imagery and easy navigation"
            },
            {
                "name": "Expense Tracker",
                "description": "Personal finance app for tracking expenses with categories and budgets",
                "features": "Expense logging, categories, budgets, charts, export data",
                "style": "Professional, clean interface with data visualization"
            }
        ]
    }

# Background processing functions
async def process_app_generation(job_id: int, request_data: Dict[str, Any]):
    """Process app generation in background"""
    try:
        # Generate the app
        generated_app = await ai_code_generator.generate_app(
            description=request_data["description"],
            app_type=request_data["app_type"],
            features=request_data["features"],
            style=request_data["style"],
            framework=request_data["framework"]
        )
        
        # Update job with results
        # This would need database access - simplified for now
        output_data = {
            "app_id": generated_app.app_id,
            "name": generated_app.name,
            "description": generated_app.description,
            "framework": generated_app.framework,
            "files": generated_app.files,
            "metadata": generated_app.metadata
        }
        
        # In real implementation, update job status to COMPLETED
        # and set output_data
        
    except Exception as e:
        # In real implementation, update job status to FAILED
        # and set error_message
        pass

async def process_app_deployment(job_id: int, app_id: str, deployment_config: Dict[str, Any]):
    """Process app deployment in background"""
    try:
        # Deploy the app
        deployment_url = f"https://{app_id}.{deployment_config['platform']}.app"
        
        # Update job with deployment URL
        # This would need database access - simplified for now
        
    except Exception as e:
        # Handle deployment errors
        pass
