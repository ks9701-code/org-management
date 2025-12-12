from typing import Optional
from bson import ObjectId
from datetime import timedelta
from app.core.database import get_master_db
from app.core.security import verify_password, create_access_token
from app.core.config import settings


class AuthService:
    """Service for handling authentication."""
    
    @staticmethod
    async def login(email: str, password: str) -> dict:
        """Authenticate admin user and return JWT token."""
        master_db = await get_master_db()
        
        # Find admin user
        admin_doc = await master_db.admin_users.find_one({"email": email})
        if not admin_doc:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not verify_password(password, admin_doc["hashed_password"]):
            raise ValueError("Invalid email or password")
        
        # Get organization details
        org_doc = await master_db.organizations.find_one(
            {"organization_name": admin_doc["organization_name"]}
        )
        if not org_doc:
            raise ValueError("Organization not found for admin user")
        
        # Create JWT token
        token_data = {
            "admin_id": str(admin_doc["_id"]),
            "organization_id": str(org_doc["_id"]),
            "organization_name": admin_doc["organization_name"],
            "email": email
        }
        
        expires_delta = timedelta(minutes=settings.jwt_expire_minutes)
        access_token = create_access_token(token_data, expires_delta)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "admin_id": str(admin_doc["_id"]),
            "organization_id": str(org_doc["_id"]),
            "organization_name": admin_doc["organization_name"]
        }
    
    @staticmethod
    async def get_current_admin(token: str) -> Optional[dict]:
        """Get current admin user from JWT token."""
        from app.core.security import decode_access_token
        
        payload = decode_access_token(token)
        if not payload:
            return None
        
        master_db = await get_master_db()
        admin_doc = await master_db.admin_users.find_one(
            {"_id": ObjectId(payload.get("admin_id"))}
        )
        
        if not admin_doc:
            return None
        
        return {
            "admin_id": str(admin_doc["_id"]),
            "email": admin_doc["email"],
            "organization_name": admin_doc["organization_name"],
            "organization_id": admin_doc["organization_id"]
        }

