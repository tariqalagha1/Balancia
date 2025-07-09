import pytest
from fastapi import status
from backend.core.models import User
from backend.core.schemas import UserCreate

def test_login_success(client, test_db):
    # Create test user
    test_user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        tenant_id="test-tenant"
    )
    test_db.add(test_user)
    test_db.commit()

    # Test login
    response = client.post("/token", data={"username": "testuser", "password": "secret"})
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post("/token", data={"username": "nonexistent", "password": "wrong"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["error"] == "authentication_error"

def test_register_user(client, test_db):
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "secret",
        "role_id": 1
    }
    response = client.post("/register", json=user_data, headers={"X-Tenant-ID": "test-tenant"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "newuser"

def test_register_duplicate_username(client, test_db):
    # Create existing user
    test_user = User(
        username="existing",
        email="existing@example.com",
        hashed_password="hashed",
        tenant_id="test-tenant"
    )
    test_db.add(test_user)
    test_db.commit()

    # Try to register same username
    user_data = {
        "username": "existing",
        "email": "new@example.com",
        "password": "secret",
        "role_id": 1
    }
    response = client.post("/register", json=user_data, headers={"X-Tenant-ID": "test-tenant"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["error"] == "validation_error"