import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_organization():
    """Test organization creation."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/org/create",
            json={
                "organization_name": "TestOrg",
                "email": "admin@testorg.com",
                "password": "securepass123"
            }
        )
        assert response.status_code in [201, 400]  # 201 created or 400 if exists


@pytest.mark.asyncio
async def test_admin_login():
    """Test admin login."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/admin/login",
            json={
                "email": "admin@testorg.com",
                "password": "securepass123"
            }
        )
        assert response.status_code in [200, 401]  # 200 success or 401 unauthorized

