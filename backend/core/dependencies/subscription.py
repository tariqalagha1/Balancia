from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import Tenant
from core.services.auth import get_current_user


def enforce_subscription(module_name: str):
    """
    FastAPI dependency to enforce module access and user count limits based on tenant subscription.
    Usage: Depends(enforce_subscription("crm"))
    """

    def checker(
        db: Session = Depends(get_db),
        tenant_id: int = Depends(
            lambda: None
        ),  # get_tenant_id should be injected in router
        current_user=Depends(get_current_user),
    ):
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant or not tenant.subscription:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="No active subscription for tenant.",
            )
        allowed_modules = tenant.subscription.allowed_modules or []
        if module_name not in allowed_modules:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Module '{module_name}' not included in subscription.",
            )
        if tenant.current_user_count > tenant.subscription.max_users:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Maximum user count for tenant exceeded.",
            )
        return True

    return checker
