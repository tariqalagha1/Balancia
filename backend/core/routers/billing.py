import os

import stripe
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Subscription, User
from ..schemas import StripeCustomerCreate, StripeSubscriptionCreate
from ..services.billing import (create_stripe_customer,
                                create_stripe_subscription,
                                handle_stripe_webhook)
from core.services.auth import require_role

router = APIRouter()

# Load Stripe API key from environment
stripe.api_key = os.getenv("STRIPE_API_KEY")


@router.post("/create-customer/")
async def create_customer(
    data: StripeCustomerCreate, 
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin", "Staff"))
):
    """
    Create a Stripe customer for a user
    """
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        customer = create_stripe_customer(user, db)
        return {"customer_id": customer.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/create-subscription/")
async def create_subscription(
    data: StripeSubscriptionCreate, 
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin", "Staff"))
):
    """
    Create a Stripe subscription for a user
    """
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    plan = db.query(Subscription).filter(Subscription.id == data.plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    try:
        subscription = create_stripe_subscription(user, plan, db)
        return {"subscription_id": subscription.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stripe-webhook/")
async def stripe_webhook(
    request: Request, 
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Admin", "Staff"))
):
    """
    Handle Stripe webhook events
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = handle_stripe_webhook(payload, sig_header, db)
        return {"status": "success", "event": event.type}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
