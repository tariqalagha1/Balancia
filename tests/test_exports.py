import pytest
from fastapi import status
from io import BytesIO
from backend.core.models import User, Role
from backend.core.routers.export import router as export_router

def test_pdf_export(client, test_db):
    # Create test user with export permission
    export_role = Role(name="export", permissions=["export"])
    test_db.add(export_role)
    test_db.commit()

    export_user = User(
        username="exportuser",
        email="export@example.com",
        hashed_password="hashed",
        tenant_id="test-tenant",
        role_id=export_role.id
    )
    test_db.add(export_user)
    test_db.commit()

    # Get auth token
    token = client.post("/token",
        data={"username": "exportuser", "password": "secret"},
        headers={"X-Tenant-ID": "test-tenant"}
    ).json()["access_token"]

    # Test PDF export
    response = client.get("/export/pdf",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": "test-tenant"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment; filename=export.pdf" in response.headers["content-disposition"]

def test_excel_export(client, test_db):
    # Test without proper permissions
    regular_user = User(
        username="regular",
        email="regular@example.com",
        hashed_password="hashed",
        tenant_id="test-tenant"
    )
    test_db.add(regular_user)
    test_db.commit()

    token = client.post("/token",
        data={"username": "regular", "password": "secret"},
        headers={"X-Tenant-ID": "test-tenant"}
    ).json()["access_token"]

    response = client.get(
        "/export/excel",
        headers={
            "Authorization": f"Bearer {token}",
            "X-Tenant-ID": "test-tenant"
        }
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["error"] == "authorization_error"