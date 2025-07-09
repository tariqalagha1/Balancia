from typing import Optional

from fastapi import Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.database import get_db
from core.middleware import get_tenant


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role_id: int


class UserInviteCreate(BaseModel):
    email: str
    role_id: int


class User(BaseModel):
    id: int
    username: str
    email: str
    role_id: int
    tenant_id: int
    invited_by: Optional[int] = None
    invitation_status: Optional[str] = None
    is_active: bool = True

    class Config:
        orm_mode = True


# Dependency to get tenant with subscription validation
def get_tenant_dep(request: Request, db: Session = Depends(get_db)):
    return get_tenant(request, db)
