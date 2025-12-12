from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import AdminLogin, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def admin_login(login_data: AdminLogin):
    """Admin login endpoint. Returns JWT token."""
    try:
        result = await AuthService.login(
            email=login_data.email,
            password=login_data.password
        )
        return TokenResponse(
            access_token=result["access_token"],
            token_type=result["token_type"],
            admin_id=result["admin_id"],
            organization_id=result["organization_id"],
            organization_name=result["organization_name"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

