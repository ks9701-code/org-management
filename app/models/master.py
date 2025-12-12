from typing import Optional
from datetime import datetime
from bson import ObjectId


class Organization:
    """Organization document structure in master database."""
    
    def __init__(
        self,
        organization_name: str,
        collection_name: str,
        admin_email: str,
        admin_id: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.organization_name = organization_name
        self.collection_name = collection_name
        self.admin_email = admin_email
        self.admin_id = admin_id
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB insertion."""
        return {
            "organization_name": self.organization_name,
            "collection_name": self.collection_name,
            "admin_email": self.admin_email,
            "admin_id": self.admin_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create Organization instance from MongoDB document."""
        return cls(
            organization_name=data["organization_name"],
            collection_name=data["collection_name"],
            admin_email=data["admin_email"],
            admin_id=data["admin_id"],
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


class AdminUser:
    """Admin user document structure in master database."""
    
    def __init__(
        self,
        email: str,
        hashed_password: str,
        organization_name: str,
        organization_id: str,
        created_at: Optional[datetime] = None
    ):
        self.email = email
        self.hashed_password = hashed_password
        self.organization_name = organization_name
        self.organization_id = organization_id
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MongoDB insertion."""
        return {
            "email": self.email,
            "hashed_password": self.hashed_password,
            "organization_name": self.organization_name,
            "organization_id": self.organization_id,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create AdminUser instance from MongoDB document."""
        return cls(
            email=data["email"],
            hashed_password=data["hashed_password"],
            organization_name=data["organization_name"],
            organization_id=str(data.get("_id", "")),
            created_at=data.get("created_at")
        )

