from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.org import (
    OrganizationCreate,
    OrganizationResponse,
    OrganizationUpdate
)
from app.services.org_service import OrganizationService
from app.api.deps import get_current_admin

router = APIRouter(prefix="/org", tags=["organizations"])


@router.post("/create", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(org_data: OrganizationCreate):
    """Create a new organization with dynamic MongoDB collection."""
    try:
        # DEBUG: Verify what we received from the request
        import sys
        password_received = org_data.password
        if not isinstance(password_received, str):
            error_msg = f"DEBUG: API route received non-string password. Type: {type(password_received)}"
            print(error_msg, file=sys.stderr)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid password type: {type(password_received).__name__}"
            )
        
        if len(password_received) > 100:
            error_msg = f"DEBUG: API route received suspiciously long password. Length: {len(password_received)}. First 100: {password_received[:100]}"
            print(error_msg, file=sys.stderr)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password appears incorrect. Length: {len(password_received)} chars."
            )
        
        # Extract ONLY the password string
        password_to_pass = str(password_received).strip()
        
        result = await OrganizationService.create_organization(
            organization_name=org_data.organization_name,
            email=org_data.email,
            password=password_to_pass
        )
        return OrganizationResponse(
            organization_name=result["organization_name"],
            collection_name=result["collection_name"],
            admin_email=result["admin_email"],
            created_at=result["created_at"],
            updated_at=result["created_at"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create organization: {str(e)}"
        )


@router.get("/get", response_model=OrganizationResponse)
async def get_organization(
    organization_name: str = Query(..., description="Name of the organization to retrieve")
):
    """Get organization details by name."""
    org = await OrganizationService.get_organization(organization_name)
    
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization '{organization_name}' not found"
        )
    
    return OrganizationResponse(
        organization_name=org["organization_name"],
        collection_name=org["collection_name"],
        admin_email=org["admin_email"],
        created_at=org["created_at"],
        updated_at=org["updated_at"]
    )


@router.put("/update", response_model=OrganizationResponse)
async def update_organization(
    org_data: OrganizationUpdate,
    current_admin: dict = Depends(get_current_admin)
):
    """Update organization details. Requires authentication."""
    try:
        # Verify admin belongs to the organization being updated
        # (check current org name, not the potentially new one)
        if current_admin["organization_name"] != org_data.organization_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own organization"
            )
        
        # If renaming, verify admin will still own the new organization
        if org_data.new_organization_name and org_data.new_organization_name != org_data.organization_name:
            # Admin is renaming their own org, which is allowed
            pass
        
        result = await OrganizationService.update_organization(
            organization_name=org_data.organization_name,
            new_email=org_data.email,
            new_password=org_data.password,
            new_organization_name=org_data.new_organization_name
        )
        
        return OrganizationResponse(
            organization_name=result["organization_name"],
            collection_name=result["collection_name"],
            admin_email=result["admin_email"],
            created_at=result["created_at"],
            updated_at=result["updated_at"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update organization: {str(e)}"
        )


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_organization(
    organization_name: str = Query(..., description="Name of the organization to delete"),
    current_admin: dict = Depends(get_current_admin)
):
    """Delete organization and its collection. Requires authentication."""
    try:
        # Verify admin belongs to the organization being deleted
        if current_admin["organization_name"] != organization_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own organization"
            )
        
        await OrganizationService.delete_organization(organization_name)
        return {"message": f"Organization '{organization_name}' deleted successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete organization: {str(e)}"
        )

