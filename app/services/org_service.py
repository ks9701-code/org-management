from typing import Optional
from bson import ObjectId
from app.core.database import get_master_db, get_org_collection
from app.core.security import hash_password
from app.models.master import Organization, AdminUser
from app.utils.naming import slugify_org_name


class OrganizationService:
    """Service for managing organizations and their dynamic collections."""
    
    @staticmethod
    async def create_organization(organization_name: str, email: str, password: str) -> dict:
        """Create a new organization with dynamic collection."""
        master_db = await get_master_db()
        
        # Check if organization already exists
        existing_org = await master_db.organizations.find_one(
            {"organization_name": organization_name}
        )
        if existing_org:
            raise ValueError(f"Organization '{organization_name}' already exists")
        
        # Check if email already exists
        existing_admin = await master_db.admin_users.find_one({"email": email})
        if existing_admin:
            raise ValueError(f"Email '{email}' is already registered")
        
        # Generate collection name
        collection_name = slugify_org_name(organization_name)
        
        # DEBUG: Verify password before hashing
        import sys
        if not isinstance(password, str):
            error_msg = f"DEBUG: org_service.create_organization received non-string password. Type: {type(password)}, Value: {str(password)[:100]}"
            print(error_msg, file=sys.stderr)
            raise ValueError(f"Password must be a string. Received: {type(password).__name__}")
        
        if len(password) > 100:
            error_msg = f"DEBUG: org_service received suspiciously long password. Length: {len(password)} chars. First 100: {password[:100]}"
            print(error_msg, file=sys.stderr)
            raise ValueError(f"Password appears incorrect. Length: {len(password)} chars. Expected short password string.")
        
        # Hash password - ensure we're passing ONLY the password string
        password_to_hash = str(password).strip()
        hashed_password = hash_password(password_to_hash)
        
        # Create admin user first
        admin_user = AdminUser(
            email=email,
            hashed_password=hashed_password,
            organization_name=organization_name,
            organization_id=""  # Will be set after insertion
        )
        admin_result = await master_db.admin_users.insert_one(admin_user.to_dict())
        admin_id = str(admin_result.inserted_id)
        
        # Create organization document
        org = Organization(
            organization_name=organization_name,
            collection_name=collection_name,
            admin_email=email,
            admin_id=admin_id
        )
        org_result = await master_db.organizations.insert_one(org.to_dict())
        org_id = str(org_result.inserted_id)
        
        # Update admin user with organization_id
        await master_db.admin_users.update_one(
            {"_id": ObjectId(admin_id)},
            {"$set": {"organization_id": org_id}}
        )
        
        # Create dynamic collection (initialize with empty document or schema)
        org_collection = await get_org_collection(organization_name)
        # Initialize collection with a metadata document
        await org_collection.insert_one({
            "_metadata": {
                "organization_name": organization_name,
                "created_at": org.created_at,
                "collection_name": collection_name
            }
        })
        
        return {
            "organization_id": org_id,
            "organization_name": organization_name,
            "collection_name": collection_name,
            "admin_email": email,
            "admin_id": admin_id,
            "created_at": org.created_at
        }
    
    @staticmethod
    async def get_organization(organization_name: str) -> Optional[dict]:
        """Get organization details from master database."""
        master_db = await get_master_db()
        org_doc = await master_db.organizations.find_one(
            {"organization_name": organization_name}
        )
        
        if not org_doc:
            return None
        
        return {
            "organization_id": str(org_doc["_id"]),
            "organization_name": org_doc["organization_name"],
            "collection_name": org_doc["collection_name"],
            "admin_email": org_doc["admin_email"],
            "admin_id": org_doc["admin_id"],
            "created_at": org_doc["created_at"],
            "updated_at": org_doc["updated_at"]
        }
    
    @staticmethod
    async def update_organization(
        organization_name: str,
        new_email: Optional[str] = None,
        new_password: Optional[str] = None,
        new_organization_name: Optional[str] = None
    ) -> dict:
        """Update organization details."""
        master_db = await get_master_db()
        
        # Get existing organization
        org_doc = await master_db.organizations.find_one(
            {"organization_name": organization_name}
        )
        if not org_doc:
            raise ValueError(f"Organization '{organization_name}' does not exist")
        
        org_id = str(org_doc["_id"])
        old_collection_name = org_doc["collection_name"]
        update_data = {}
        
        # Handle organization name change (requires collection migration)
        if new_organization_name and new_organization_name != organization_name:
            # Check if new name already exists
            existing = await master_db.organizations.find_one(
                {"organization_name": new_organization_name}
            )
            if existing:
                raise ValueError(f"Organization '{new_organization_name}' already exists")
            
            new_collection_name = slugify_org_name(new_organization_name)
            update_data["organization_name"] = new_organization_name
            update_data["collection_name"] = new_collection_name
            
            # Migrate data from old collection to new collection
            old_collection = await get_org_collection(organization_name)
            new_collection = await get_org_collection(new_organization_name)
            
            # Copy all documents from old to new collection
            async for doc in old_collection.find({}):
                doc.pop("_id", None)  # Remove _id to allow MongoDB to generate new one
                await new_collection.insert_one(doc)
            
            # Drop old collection
            await old_collection.drop()
            
            # Update organization name in admin_users
            await master_db.admin_users.update_many(
                {"organization_name": organization_name},
                {"$set": {"organization_name": new_organization_name}}
            )
        
        # Update email if provided
        if new_email:
            # Check if email already exists for different org
            existing_admin = await master_db.admin_users.find_one({
                "email": new_email,
                "organization_name": {"$ne": organization_name}
            })
            if existing_admin:
                raise ValueError(f"Email '{new_email}' is already registered to another organization")
            
            update_data["admin_email"] = new_email
            await master_db.admin_users.update_one(
                {"organization_id": org_id},
                {"$set": {"email": new_email}}
            )
        
        # Update password if provided
        if new_password:
            hashed_password = hash_password(new_password)
            await master_db.admin_users.update_one(
                {"organization_id": org_id},
                {"$set": {"hashed_password": hashed_password}}
            )
        
        # Update organization metadata
        if update_data:
            update_data["updated_at"] = org_doc.get("updated_at")
            await master_db.organizations.update_one(
                {"_id": ObjectId(org_id)},
                {"$set": update_data}
            )
        
        # Return updated organization
        return await OrganizationService.get_organization(
            new_organization_name if new_organization_name else organization_name
        )
    
    @staticmethod
    async def delete_organization(organization_name: str) -> bool:
        """Delete organization and its collection."""
        master_db = await get_master_db()
        
        # Get organization
        org_doc = await master_db.organizations.find_one(
            {"organization_name": organization_name}
        )
        if not org_doc:
            raise ValueError(f"Organization '{organization_name}' does not exist")
        
        org_id = str(org_doc["_id"])
        admin_id = org_doc["admin_id"]
        collection_name = org_doc["collection_name"]
        
        # Drop organization collection
        org_collection = await get_org_collection(organization_name)
        await org_collection.drop()
        
        # Delete admin user
        await master_db.admin_users.delete_one({"_id": ObjectId(admin_id)})
        
        # Delete organization metadata
        await master_db.organizations.delete_one({"_id": ObjectId(org_id)})
        
        return True

