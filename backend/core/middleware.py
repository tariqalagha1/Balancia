from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from .database import get_db
from .models import Subscription, Tenant


async def get_tenant(request: Request, db: Session = Depends(get_db)):
    """
    Extract and validate tenant from request headers with subscription checks.

    Requires:
    - X-Tenant-ID header with valid tenant ID
    - Tenant must exist in database
    - Active subscription with module access

    Returns:
    - Validated tenant object

    Raises:
    - HTTP 400 if header missing or invalid format
    - HTTP 404 if tenant not found
    - HTTP 403 if subscription invalid or module not allowed
    """
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Tenant-ID header is required",
        )

    try:
        tenant_id = int(tenant_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid tenant ID format"
        )

    # Get tenant and subscription
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found"
        )

    subscription = (
        db.query(Subscription).filter(Subscription.id == tenant.subscription_id).first()
    )

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No active subscription"
        )

    # Check module access
    module = request.url.path.split("/")[2]  # /api/{module}/...
    allowed_modules = subscription.allowed_modules.split(",")
    if module not in allowed_modules and not request.url.path.startswith("/auth"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Module not included in subscription",
        )

    # Check user limit
    if tenant.current_user_count >= subscription.max_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Maximum user limit reached"
        )

    return tenant


def tenant_middleware(app):
    """Middleware to validate tenant subscription for all requests"""

    @app.middleware("http")
    async def validate_tenant(request: Request, call_next):
        # Skip tenant validation for auth endpoints
        if request.url.path.startswith("/auth"):
            return await call_next(request)

        try:
            # This will validate tenant and subscription
            await get_tenant(request, next(get_db()))
        except HTTPException as e:
            raise e

        response = await call_next(request)
        return response

    return app


def get_tenant_id(request: Request):
    return request.state.tenant_id
