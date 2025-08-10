"""
Seed script to create initial data for development
"""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .database import AsyncSessionLocal
from .models import Tenant, User, Membership, Project, UserRole

async def seed_data():
    """Create initial seed data"""
    async with AsyncSessionLocal() as db:
        # Check if tenant already exists
        result = await db.execute(select(Tenant).where(Tenant.slug == "default"))
        tenant = result.scalar_one_or_none()
        
        if not tenant:
            # Create default tenant
            tenant = Tenant(
                name="Default Organization",
                slug="default"
            )
            db.add(tenant)
            await db.commit()
            await db.refresh(tenant)
            print(f"Created tenant: {tenant.name}")
        
        # Check if user exists
        result = await db.execute(select(User).where(User.email == "admin@aeon.dev"))
        user = result.scalar_one_or_none()
        
        if not user:
            # Create default user
            user = User(
                external_identity_id="dev_admin_001",
                email="admin@aeon.dev",
                name="Admin User"
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            print(f"Created user: {user.email}")
        
        # Check if membership exists
        result = await db.execute(
            select(Membership).where(
                Membership.tenant_id == tenant.id,
                Membership.user_id == user.id
            )
        )
        membership = result.scalar_one_or_none()
        
        if not membership:
            # Create membership
            membership = Membership(
                tenant_id=tenant.id,
                user_id=user.id,
                role=UserRole.ADMIN,
                status="active"
            )
            db.add(membership)
            await db.commit()
            print(f"Created membership for {user.email} in {tenant.name}")
        
        # Check if project exists
        result = await db.execute(
            select(Project).where(
                Project.tenant_id == tenant.id,
                Project.name == "Default Media Project"
            )
        )
        project = result.scalar_one_or_none()
        
        if not project:
            # Create default project
            project = Project(
                tenant_id=tenant.id,
                name="Default Media Project",
                description="Default project for media generation",
                type="media",
                settings={"auto_created": True}
            )
            db.add(project)
            await db.commit()
            print(f"Created project: {project.name}")
        
        print("Seed data creation complete!")

if __name__ == "__main__":
    asyncio.run(seed_data())
