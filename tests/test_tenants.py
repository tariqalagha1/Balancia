import pytest
from fastapi import status
from backend.core.models import User

def test_tenant_middleware_required(client):
    # Test without tenant header
    response = client.get("/protected")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "http_error"

def test_tenant_isolation(client, test_db):
    # Create users in different tenants
    user1 = User(
        username="user1",
        email="user1@example.com",
        hashed_password="hashed1",
        tenant_id="tenant1"
    )
    user2 = User(
        username="user2",
        email="user2@example.com", 
        hashed_password="hashed2",
        tenant_id="tenant2"
    )
    test_db.add_all([user1, user2])
    test_db.commit()

    # Login user1
    login_response = client.post("/token",
        data={"username": "user1", "password": "secret"},
        headers={"X-Tenant-ID": "tenant1"}
    )
    token = login_response.json()["access_token"]

    # Access protected route with correct tenant
    protected_response = client.get("/protected",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": "tenant1"
        }
    )
    assert protected_response.status_code == status.HTTP_200_OK
    assert protected_response.json()["tenant"] == "tenant1"

    # Try to access with wrong tenant
    wrong_tenant_response = client.get("/protected",
        headers={
            "Authorization": f"Bearer {token}", 
            "X-Tenant-ID": "tenant2"
        }
    )
    assert wrong_tenant_response.status_code == status.HTTP_401_UNAUTHORIZED