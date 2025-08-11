"""
Business Integration API Routes
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..database import get_db, Integration, Job, JobStatus, JobType
from ..auth import get_current_user, AuthenticatedUser
from ..integrations.crm_integrations import CRMIntegrationFactory, CRMProvider
from ..integrations.ecommerce_integrations import EcommerceIntegrationFactory, EcommerceProvider
from ..schemas import IntegrationResponse, IntegrationCreateInput, JobResponse

router = APIRouter(prefix="/v1/integrations", tags=["Business Integrations"])

# CRM Integrations
@router.post("/crm/hubspot/connect", response_model=IntegrationResponse)
async def connect_hubspot(
    integration_data: IntegrationCreateInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Connect HubSpot CRM integration"""
    try:
        integration = Integration(
            tenant_id=current_user.tenant_id,
            provider="hubspot",
            name=integration_data.name,
            credentials=integration_data.credentials,
            settings=integration_data.settings or {},
            created_by=current_user.user_id
        )
        db.add(integration)
        await db.commit()
        await db.refresh(integration)
        
        return IntegrationResponse(
            id=integration.id,
            provider=integration.provider,
            name=integration.name,
            is_active=integration.is_active,
            last_sync=integration.last_sync,
            created_at=integration.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect HubSpot: {str(e)}")

@router.post("/crm/salesforce/connect", response_model=IntegrationResponse)
async def connect_salesforce(
    integration_data: IntegrationCreateInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Connect Salesforce CRM integration"""
    try:
        integration = Integration(
            tenant_id=current_user.tenant_id,
            provider="salesforce",
            name=integration_data.name,
            credentials=integration_data.credentials,
            settings=integration_data.settings or {},
            created_by=current_user.user_id
        )
        db.add(integration)
        await db.commit()
        await db.refresh(integration)
        
        return IntegrationResponse(
            id=integration.id,
            provider=integration.provider,
            name=integration.name,
            is_active=integration.is_active,
            last_sync=integration.last_sync,
            created_at=integration.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect Salesforce: {str(e)}")

@router.post("/crm/pipedrive/connect", response_model=IntegrationResponse)
async def connect_pipedrive(
    integration_data: IntegrationCreateInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Connect Pipedrive CRM integration"""
    try:
        integration = Integration(
            tenant_id=current_user.tenant_id,
            provider="pipedrive",
            name=integration_data.name,
            credentials=integration_data.credentials,
            settings=integration_data.settings or {},
            created_by=current_user.user_id
        )
        db.add(integration)
        await db.commit()
        await db.refresh(integration)
        
        return IntegrationResponse(
            id=integration.id,
            provider=integration.provider,
            name=integration.name,
            is_active=integration.is_active,
            last_sync=integration.last_sync,
            created_at=integration.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect Pipedrive: {str(e)}")

# E-commerce Integrations
@router.post("/ecommerce/shopify/connect", response_model=IntegrationResponse)
async def connect_shopify(
    integration_data: IntegrationCreateInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Connect Shopify store integration"""
    try:
        integration = Integration(
            tenant_id=current_user.tenant_id,
            provider="shopify",
            name=integration_data.name,
            credentials=integration_data.credentials,
            settings=integration_data.settings or {},
            created_by=current_user.user_id
        )
        db.add(integration)
        await db.commit()
        await db.refresh(integration)
        
        return IntegrationResponse(
            id=integration.id,
            provider=integration.provider,
            name=integration.name,
            is_active=integration.is_active,
            last_sync=integration.last_sync,
            created_at=integration.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect Shopify: {str(e)}")

@router.post("/ecommerce/woocommerce/connect", response_model=IntegrationResponse)
async def connect_woocommerce(
    integration_data: IntegrationCreateInput,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Connect WooCommerce store integration"""
    try:
        integration = Integration(
            tenant_id=current_user.tenant_id,
            provider="woocommerce",
            name=integration_data.name,
            credentials=integration_data.credentials,
            settings=integration_data.settings or {},
            created_by=current_user.user_id
        )
        db.add(integration)
        await db.commit()
        await db.refresh(integration)
        
        return IntegrationResponse(
            id=integration.id,
            provider=integration.provider,
            name=integration.name,
            is_active=integration.is_active,
            last_sync=integration.last_sync,
            created_at=integration.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect WooCommerce: {str(e)}")

# Integration Actions
@router.post("/crm/{integration_id}/sync-contacts", response_model=JobResponse)
async def sync_crm_contacts(
    integration_id: int,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Sync contacts from CRM integration"""
    try:
        # Verify integration exists and belongs to tenant
        result = await db.execute(
            select(Integration).where(
                Integration.id == integration_id,
                Integration.tenant_id == current_user.tenant_id
            )
        )
        integration = result.scalar_one_or_none()
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "action": "sync_contacts",
                "integration_id": integration_id,
                "provider": integration.provider
            },
            provider=integration.provider
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_crm_sync, job.id, integration_id, "contacts")
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to sync contacts: {str(e)}")

@router.post("/ecommerce/{integration_id}/sync-products", response_model=JobResponse)
async def sync_ecommerce_products(
    integration_id: int,
    background_tasks: BackgroundTasks,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Sync products from e-commerce integration"""
    try:
        # Verify integration exists and belongs to tenant
        result = await db.execute(
            select(Integration).where(
                Integration.id == integration_id,
                Integration.tenant_id == current_user.tenant_id
            )
        )
        integration = result.scalar_one_or_none()
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        job = Job(
            tenant_id=current_user.tenant_id,
            type=JobType.AGENT_TASK,
            status=JobStatus.PENDING,
            input_data={
                "action": "sync_products",
                "integration_id": integration_id,
                "provider": integration.provider
            },
            provider=integration.provider
        )
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        background_tasks.add_task(process_ecommerce_sync, job.id, integration_id, "products")
        
        return JobResponse(
            id=job.id,
            type=job.type,
            status=job.status,
            input_data=job.input_data,
            created_at=job.created_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to sync products: {str(e)}")

# List Integrations
@router.get("/", response_model=List[IntegrationResponse])
async def list_integrations(
    provider: Optional[str] = None,
    current_user: AuthenticatedUser = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all integrations for the tenant"""
    try:
        query = select(Integration).where(Integration.tenant_id == current_user.tenant_id)
        
        if provider:
            query = query.where(Integration.provider == provider)
        
        result = await db.execute(query)
        integrations = result.scalars().all()
        
        return [
            IntegrationResponse(
                id=integration.id,
                provider=integration.provider,
                name=integration.name,
                is_active=integration.is_active,
                last_sync=integration.last_sync,
                created_at=integration.created_at
            )
            for integration in integrations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list integrations: {str(e)}")

# Background processing functions
async def process_crm_sync(job_id: int, integration_id: int, sync_type: str):
    """Process CRM synchronization"""
    pass

async def process_ecommerce_sync(job_id: int, integration_id: int, sync_type: str):
    """Process e-commerce synchronization"""
    pass
