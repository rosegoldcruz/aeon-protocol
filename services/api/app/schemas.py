from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class JobType(str, Enum):
    IMAGE_GENERATION = "image_generation"
    VIDEO_GENERATION = "video_generation"
    AUDIO_GENERATION = "audio_generation"
    AGENT_TASK = "agent_task"

class MediaType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class UserRole(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    CLIENT = "client"

# Job schemas
class JobCreate(BaseModel):
    type: JobType
    input_data: Dict[str, Any]
    project_id: Optional[int] = None

class ImageGenerationInput(BaseModel):
    prompt: str
    model: Optional[str] = "flux-schnell"
    width: Optional[int] = 1024
    height: Optional[int] = 1024
    num_outputs: Optional[int] = 1
    guidance_scale: Optional[float] = 7.5
    num_inference_steps: Optional[int] = 4

class VideoGenerationInput(BaseModel):
    prompt: str
    provider: Optional[str] = "runway"
    video_type: Optional[str] = "text_to_video"
    image_url: Optional[str] = None
    duration: Optional[int] = 5
    resolution: Optional[str] = "1280x768"
    aspect_ratio: Optional[str] = "16:9"
    motion_strength: Optional[int] = 5
    fps: Optional[int] = 24
    guidance_scale: Optional[float] = 12
    negative_prompt: Optional[str] = ""

class AudioGenerationInput(BaseModel):
    text: str
    voice_id: Optional[str] = None
    model_id: Optional[str] = "eleven_monolingual_v1"
    stability: Optional[float] = 0.5
    similarity_boost: Optional[float] = 0.5

class JobResponse(BaseModel):
    id: int
    tenant_id: int
    project_id: Optional[int]
    user_id: Optional[int]
    type: JobType
    status: JobStatus
    input_data: Dict[str, Any]
    output_data: Optional[Dict[str, Any]]
    provider: Optional[str]
    provider_job_id: Optional[str]
    cost_cents: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

class JobListResponse(BaseModel):
    jobs: List[JobResponse]
    total: int
    page: int
    per_page: int

# Asset schemas
class AssetResponse(BaseModel):
    id: int
    tenant_id: int
    project_id: Optional[int]
    job_id: Optional[int]
    s3_key: str
    s3_bucket: str
    media_type: str
    file_type: Optional[str]
    file_size: Optional[int]
    width: Optional[int]
    height: Optional[int]
    duration: Optional[int]
    metadata_json: Optional[Dict[str, Any]]
    created_at: datetime
    presigned_url: Optional[str] = None

    class Config:
        from_attributes = True

# Tenant schemas
class TenantResponse(BaseModel):
    id: int
    name: str
    slug: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# User schemas
class UserResponse(BaseModel):
    id: int
    external_identity_id: str
    email: str
    name: Optional[str]
    avatar_url: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Project schemas
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: Optional[str] = "media"
    settings: Optional[Dict[str, Any]] = None

class ProjectResponse(BaseModel):
    id: int
    tenant_id: int
    name: str
    description: Optional[str]
    type: Optional[str]
    settings: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Error schemas
class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None

# AI Agent Schemas
class AgentTaskInput(BaseModel):
    task: str
    parameters: Dict[str, Any] = {}

class AgentResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str] = None
    configuration: Dict[str, Any] = {}
    is_active: bool
    created_at: datetime

# Integration Schemas
class IntegrationCreateInput(BaseModel):
    name: str
    credentials: Dict[str, Any]
    settings: Optional[Dict[str, Any]] = None

class IntegrationResponse(BaseModel):
    id: int
    provider: str
    name: str
    is_active: bool
    last_sync: Optional[datetime] = None
    created_at: datetime

# Workflow Schemas
class WorkflowCreateInput(BaseModel):
    name: str
    description: Optional[str] = None
    definition: Dict[str, Any]
    is_active: bool = True

class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    definition: Dict[str, Any]
    is_active: bool
    trigger_count: int
    success_count: int
    error_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
