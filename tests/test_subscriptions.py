import pytest
from fastapi import status
from backend.core.models import Tenant, SubscriptionPlan
from backend.core.services.subscription import check_subscription

def test_subscription_limits(client, test_db):
    # Create test subscription plans
    basic_plan = SubscriptionPlan(
        name="Basic",
        module_access={"crm": True, "inventory": False, "accounting": False},
        max_users=5
    )
    premium_plan = SubscriptionPlan(
        name="Premium",
        module_access={"crm": True, "inventory": True, "accounting": True},
        max_users=50
    )
    test_db.add_all([basic_plan, premium_plan])
    test_db.commit()

    # Create tenants with different plans
    basic_tenant = Tenant(
        name="Basic Tenant",
        subscription_plan_id=basic_plan.id
    )
    premium_tenant = Tenant(
        name="Premium Tenant",
        subscription_plan_id=premium_plan.id
    )
    test_db.add_all([basic_tenant, premium_tenant])
    test_db.commit()

    # Test module access
    assert check_subscription(basic_tenant.id, "crm") is True
    assert check_subscription(basic_tenant.id, "inventory") is False
    assert check_subscription(premium_tenant.id, "inventory") is True

    # Test user limit enforcement
    for i in range(5):
        user = User(
            username=f"user{i}",
            email=f"user{i}@basic.com",
            hashed_password="hashed",
            tenant_id=basic_tenant.id
        )
        test_db.add(user)
    test_db.commit()

    # Should fail when exceeding user limit
    with pytest.raises(APIError) as exc_info:
        check_subscription(basic_tenant.id, "crm", new_user=True)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert "user limit" in exc_info.value.detail.lower()