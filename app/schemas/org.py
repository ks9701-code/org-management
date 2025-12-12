from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class OrganizationCreate(BaseModel):
    organization_name: str
    email: EmailStr
    password: str


class OrganizationUpdate(BaseModel):
    organization_name: str  # Current organization name (identifier)
    email: EmailStr
    password: str
    new_organization_name: Optional[str] = None  # Optional: rename organization


class OrganizationResponse(BaseModel):
    organization_name: str
    collection_name: str
    admin_email: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrganizationGet(BaseModel):
    organization_name: str


class OrganizationDelete(BaseModel):
    organization_name: str

