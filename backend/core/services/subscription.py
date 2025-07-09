from sqlalchemy.orm import Session

from ..models import Subscription, Tenant
from ..schemas import SubscriptionCreate, SubscriptionUpdate


def create_subscription(db: Session, subscription: SubscriptionCreate):
    db_subscription = Subscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription


def get_subscription(db: Session, subscription_id: int):
    return db.query(Subscription).filter(Subscription.id == subscription_id).first()


def update_subscription(
    db: Session, subscription_id: int, subscription: SubscriptionUpdate
):
    db_subscription = (
        db.query(Subscription).filter(Subscription.id == subscription_id).first()
    )
    if db_subscription:
        for key, value in subscription.dict().items():
            setattr(db_subscription, key, value)
        db.commit()
        db.refresh(db_subscription)
    return db_subscription


def delete_subscription(db: Session, subscription_id: int):
    db_subscription = (
        db.query(Subscription).filter(Subscription.id == subscription_id).first()
    )
    if db_subscription:
        db.delete(db_subscription)
        db.commit()
    return db_subscription


def calculate_usage(db: Session, tenant_id: int):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant or not tenant.subscription:
        return None

    return {
        "current_users": tenant.current_user_count,
        "max_users": tenant.subscription.max_users,
        "price_per_user": tenant.subscription.price_per_user,
        "total_due": tenant.current_user_count * tenant.subscription.price_per_user,
        "allowed_modules": tenant.subscription.allowed_modules,
    }


def upgrade_plan(db: Session, tenant_id: int, new_subscription_id: int):
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if tenant:
        tenant.subscription_id = new_subscription_id
        db.commit()
        db.refresh(tenant)
    return tenant
