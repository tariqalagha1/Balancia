import pytest
from fastapi import status
from backend.core.models import User, Role
from backend.core.dependencies.rbac import require_role

def test_rbac_access(client, test_db):
    # Create test roles and users
    admin_role = Role(name="admin", permissions=["*"])
    user_role = Role(name="user", permissions=["read"])
    test_db.add_all([admin_role, user_role])
    test_db.commit()

    admin_user = User(
        username="admin",
        email="admin@example.com",
        hashed_password="hashed",
        tenant_id="test-tenant",
        role_id=admin_role.id
    )
    regular_user = User(
        username="user",
        email="user@example.com",
        hashed_password="hashed",
        tenant_id="test-tenant",
        role_id=user_role.id
    )
    test_db.add_all([admin_user, regular_user])
    test_db.commit()

    # Test admin access
    admin_token = client.post("/token",
        data={"username": "admin", "password": "secret"},
        headers={"X-Tenant-ID": "test-tenant"}
    ).json()["access_token"]

    # Test user access
    user_token = client.post("/token",
        data={"username": "user", "password": "secret"},
        headers={"X-Tenant-ID": "test-tenant"}
    ).json()["access_token"]

    # Mock protected endpoint with require_role decorator
    @require_role("admin")
    def admin_only():
        return {"message": "Admin access granted"}

    app.add_api_route("/admin-only", admin_only, methods=["GET"])

    # Verify access
    admin_response = client.get("/admin-only",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "X-Tenant-ID": "test-tenant"
        }
    )
    assert admin_response.status_code == status.HTTP_200_OK

    user_response = client.get("/admin-only",
        headers={
            "Authorization": f"Bearer {user_token}",
            "X-Tenant-ID": "test-tenant"
        }
    )
    assert user_response.status_code == status.HTTP_403_FORBIDDEN
    assert user_response.json()["error"] == "authorization_error"