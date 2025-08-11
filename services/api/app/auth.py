"""
Clerk JWT Authentication and Authorization
"""
import os
import jwt
import requests
from typing import Optional, Dict, Any
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone

from .database import get_db, User, Tenant, Membership, UserRole

# Clerk configuration
CLERK_PUBLISHABLE_KEY = os.getenv("NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
JWKS_URL = "https://poetic-bluebird-21.clerk.accounts.dev/.well-known/jwks.json"

# Public key for JWT verification
CLERK_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnbJXM96T3o/AeLdLmivu
DWRhLNzKjyPFviKJ1avjxniSCD/fvXBal2O8UVSEWtFwyEAUUZMyW/LzwZcCPkbf
x4m/h/UvgZ8H8yIls6kLTm7lQLpNmz5h6gVRTYzvtDwaUkeQIRP2FN0m7JGqYFKB
2n6heY1J8BwgKKtf0soU61eEI1bNd/Zkpop9Jg0XlowuZKKb2fgBElmgp50oyI4g
FxjJrwHn3ndfSbuiVLSoZHlwFQ7MgO3C0Q2zkLFmF7oV6l0ocn1wtafkfwYWIAH8
m0nXzvnfM6qKzBZZs7xweGerrE8zsDr1IKAPy1cFuNFRkwooSHF4PRLw2zdMo69y
iwIDAQAB
-----END PUBLIC KEY-----"""

security = HTTPBearer()

class AuthenticatedUser:
    """Represents an authenticated user with tenant context"""
    
    def __init__(self, user_id: str, email: str, tenant_id: int, role: UserRole):
        self.user_id = user_id
        self.email = email
        self.tenant_id = tenant_id
        self.role = role

def verify_clerk_token(token: str) -> Dict[str, Any]:
    """Verify Clerk JWT token and return claims"""
    try:
        # Decode and verify the JWT token
        decoded_token = jwt.decode(
            token,
            CLERK_PUBLIC_KEY,
            algorithms=["RS256"],
            audience=CLERK_PUBLISHABLE_KEY,
            options={"verify_exp": True}
        )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

async def get_or_create_user(
    clerk_user_id: str, 
    email: str, 
    first_name: str = None, 
    last_name: str = None,
    db: AsyncSession = None
) -> User:
    """Get existing user or create new user from Clerk data"""
    
    # Check if user exists
    result = await db.execute(
        select(User).where(User.external_identity_id == clerk_user_id)
    )
    user = result.scalar_one_or_none()
    
    if user:
        # Update user info if changed
        if user.email != email:
            user.email = email
            user.updated_at = datetime.now(timezone.utc)
            await db.commit()
        return user
    
    # Create new user
    user = User(
        external_identity_id=clerk_user_id,
        email=email,
        name=f"{first_name or ''} {last_name or ''}".strip() or None
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Create default tenant for new user
    tenant = Tenant(
        name=f"{user.name or email}'s Organization",
        slug=f"user-{user.id}"
    )
    db.add(tenant)
    await db.commit()
    await db.refresh(tenant)
    
    # Create membership
    membership = Membership(
        tenant_id=tenant.id,
        user_id=user.id,
        role=UserRole.ADMIN,
        status="active"
    )
    db.add(membership)
    await db.commit()
    
    return user

async def get_user_tenant(user_id: int, db: AsyncSession) -> Optional[Tenant]:
    """Get user's primary tenant"""
    result = await db.execute(
        select(Tenant, Membership)
        .join(Membership, Tenant.id == Membership.tenant_id)
        .where(
            Membership.user_id == user_id,
            Membership.status == "active"
        )
        .order_by(Membership.created_at.asc())  # Get first/primary tenant
    )
    row = result.first()
    return row[0] if row else None

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> AuthenticatedUser:
    """Get current authenticated user from JWT token"""
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    # Verify the token
    token_claims = verify_clerk_token(credentials.credentials)
    
    # Extract user info from token
    clerk_user_id = token_claims.get("sub")
    email = token_claims.get("email")
    first_name = token_claims.get("given_name")
    last_name = token_claims.get("family_name")
    
    if not clerk_user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims"
        )
    
    # Get or create user
    user = await get_or_create_user(
        clerk_user_id=clerk_user_id,
        email=email,
        first_name=first_name,
        last_name=last_name,
        db=db
    )
    
    # Get user's tenant
    tenant = await get_user_tenant(user.id, db)
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no active tenant"
        )
    
    # Get user's role in this tenant
    result = await db.execute(
        select(Membership).where(
            Membership.user_id == user.id,
            Membership.tenant_id == tenant.id,
            Membership.status == "active"
        )
    )
    membership = result.scalar_one_or_none()
    
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no active membership"
        )
    
    return AuthenticatedUser(
        user_id=clerk_user_id,
        email=email,
        tenant_id=tenant.id,
        role=membership.role
    )

def require_role(required_role: UserRole):
    """Dependency to require specific role"""
    def role_checker(current_user: AuthenticatedUser = Depends(get_current_user)):
        role_hierarchy = {
            UserRole.CLIENT: 1,
            UserRole.VIEWER: 2,
            UserRole.EDITOR: 3,
            UserRole.ADMIN: 4
        }

        if role_hierarchy.get(current_user.role, 0) < role_hierarchy.get(required_role, 0):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {required_role.value}"
            )
        return current_user

    return role_checker

# Convenience dependencies
require_admin = require_role(UserRole.ADMIN)
require_editor = require_role(UserRole.EDITOR)
require_viewer = require_role(UserRole.VIEWER)
