from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..models import Role, Subscription, Tenant, User
from ..schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all_users(db: Session):
    return db.query(User).join(Role).all()


def create_user(db: Session, user: UserCreate, tenant_id: int):
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

    # Check user limit
    if tenant.current_user_count >= subscription.max_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Maximum user limit reached"
        )

    # Create user
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
        role_id=user.role_id,
        tenant_id=tenant_id,
    )
    db.add(db_user)

    # Update tenant user count
    tenant.current_user_count += 1
    db.commit()
    db.refresh(db_user)

    return db_user
