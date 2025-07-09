import stripe
from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.config import settings

from ..database import get_db
from ..models import Plan, Subscription, User

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_customer(user: User, db: Session):
    """Create a Stripe customer for a user"""
    try:
        customer = stripe.Customer.create(
            email=user.email, name=user.username, metadata={"user_id": user.id}
        )
        user.stripe_customer_id = customer.id
        db.commit()
        return customer.id
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


def create_stripe_subscription(user: User, plan: Plan, db: Session):
    """Create a Stripe subscription for a user"""
    try:
        # Create customer if doesn't exist
        if not user.stripe_customer_id:
            create_stripe_customer(user, db)

        # Create subscription
        subscription = stripe.Subscription.create(
            customer=user.stripe_customer_id,
            items=[{"price": plan.stripe_price_id}],
            payment_behavior="default_incomplete",
            expand=["latest_invoice.payment_intent"],
        )
        return subscription
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


def handle_stripe_webhook(payload, sig_header):
    """Process Stripe webhook events"""
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle subscription events
    if event["type"] == "customer.subscription.created":
        handle_subscription_created(event)
    elif event["type"] == "customer.subscription.updated":
        handle_subscription_updated(event)
    elif event["type"] == "customer.subscription.deleted":
        handle_subscription_deleted(event)

    return {"status": "success"}


def handle_subscription_created(event):
    """Handle new subscription creation"""
    subscription = event["data"]["object"]
    user_id = subscription["metadata"]["user_id"]
    plan_id = subscription["metadata"]["plan_id"]

    # Create subscription in database
    db = next(get_db())
    db_sub = Subscription(
        user_id=user_id,
        plan_id=plan_id,
        stripe_subscription_id=subscription["id"],
        status="active",
    )
    db.add(db_sub)
    db.commit()


def handle_subscription_updated(event):
    """Handle subscription updates (renewals, plan changes)"""
    subscription = event["data"]["object"]
    stripe_sub_id = subscription["id"]

    db = next(get_db())
    db_sub = (
        db.query(Subscription)
        .filter(Subscription.stripe_subscription_id == stripe_sub_id)
        .first()
    )

    if db_sub:
        db_sub.status = subscription["status"]
        db.commit()


def handle_subscription_deleted(event):
    """Handle subscription cancellations"""
    subscription = event["data"]["object"]
    stripe_sub_id = subscription["id"]

    db = next(get_db())
    db_sub = (
        db.query(Subscription)
        .filter(Subscription.stripe_subscription_id == stripe_sub_id)
        .first()
    )

    if db_sub:
        db_sub.status = "canceled"
        db.commit()


def sync_plans_with_stripe(db: Session):
    """Sync local plans with Stripe products"""
    plans = db.query(Plan).all()
    for plan in plans:
        if not plan.stripe_product_id:
            # Create new Stripe product
            product = stripe.Product.create(
                name=plan.name, description=plan.description
            )
            price = stripe.Price.create(
                product=product.id,
                unit_amount=plan.price * 100,  # in cents
                currency=settings.CURRENCY,
                recurring={"interval": plan.billing_interval},
            )
            plan.stripe_product_id = product.id
            plan.stripe_price_id = price.id
            db.commit()
        else:
            # Update existing Stripe product
            stripe.Product.modify(
                plan.stripe_product_id, name=plan.name, description=plan.description
            )
            # Note: Prices are immutable - create new price if amount changes
