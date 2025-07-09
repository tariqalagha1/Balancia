import secrets
import string
from datetime import datetime, timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import UserInviteCreate
from ..services.auth import get_current_user, get_password_hash
from ..services.email import send_invite_email  # Will implement next

router = APIRouter(prefix="/invite", tags=["invites"])


def generate_invite_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


@router.post("/send")
async def send_invite(
    invite_data: UserInviteCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if user has permission to send invites
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Only admins can send invites"
        )

    # Generate token and expiration
    token = generate_invite_token()
    expires_at = datetime.utcnow() + timedelta(days=7)

    # Create user record with invite status
    db_user = User(
        email=invite_data.email,
        role_id=invite_data.role_id,
        tenant_id=current_user.tenant_id,
        invited_by=current_user.id,
        invitation_status="PENDING",
        invitation_token=token,
        invitation_sent_at=datetime.utcnow(),
        is_active=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Send email via background task
    background_tasks.add_task(
        send_invite_email,
        email=invite_data.email,
        token=token,
        inviter_name=current_user.username,
    )

    return {"message": "Invite sent successfully"}


@router.get("/accept/{token}")
async def accept_invite(token: str, db: Session = Depends(get_db)):
    user = (
        db.query(User)
        .filter(User.invitation_token == token, User.invitation_status == "PENDING")
        .first()
    )

    if not user or user.invitation_sent_at < datetime.utcnow() - timedelta(days=7):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired invite token",
        )

    if user.invitation_sent_at < datetime.utcnow() - timedelta(days=7):
        user.invitation_status = "EXPIRED"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invite has expired"
        )

    return {"email": user.email, "token": token}


@router.post("/complete")
async def complete_invite(
    username: str, password: str, token: str, db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.invitation_token == token, User.invitation_status == "PENDING")
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired invite token",
        )

    # Update user with final details
    user.username = username
    user.hashed_password = get_password_hash(password)
    user.invitation_status = "ACCEPTED"
    user.is_active = True
    db.commit()

    return {"message": "Account activated successfully"}
