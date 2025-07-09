from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import crm_service, models
from ...core import schemas
from ...core.database import get_db
from ...core.middleware import get_tenant_id
from ...core.dependencies.rbac import require_role
from ...core.services.auth import get_current_user

from ...core.dependencies.subscription import enforce_subscription

router = APIRouter()

@router.post("/contacts/", response_model=schemas.Contact)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    subscription_ok: bool = Depends(enforce_subscription("crm")),
    current_user: models.User = Depends(require_role("Admin", "Staff"))
):
    return crm_service.get_crm_service(db).create_contact(contact, tenant_id)

@router.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    subscription_ok: bool = Depends(enforce_subscription("crm")),
    current_user: models.User = Depends(require_role("Admin", "Staff", "Viewer"))
):
    return crm_service.get_crm_service(db).get_contacts(tenant_id, skip, limit)

@router.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    current_user: models.User = Depends(get_current_user)
):
    return crm_service.get_crm_service(db).get_contact(contact_id, tenant_id)

@router.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(
    contact_id: int,
    contact: schemas.ContactUpdate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    subscription_ok: bool = Depends(enforce_subscription("crm")),
    current_user: models.User = Depends(require_role("Admin", "Staff"))
):
    return crm_service.get_crm_service(db).update_contact(contact_id, contact, tenant_id)

@router.delete("/contacts/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    subscription_ok: bool = Depends(enforce_subscription("crm")),
    current_user: models.User = Depends(require_role("Admin"))
):
    return crm_service.get_crm_service(db).delete_contact(contact_id, tenant_id)

@router.post("/leads/", response_model=schemas.Lead)
def create_lead(
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    current_user: models.User = Depends(get_current_user)
):
    return crm_service.get_crm_service(db).create_lead(lead, tenant_id)

@router.get("/leads/", response_model=list[schemas.Lead])
def read_leads(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    current_user: models.User = Depends(get_current_user)
):
    return crm_service.get_crm_service(db).get_leads(tenant_id, skip, limit)

@router.get("/leads/{lead_id}", response_model=schemas.Lead)
def read_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    current_user: models.User = Depends(get_current_user)
):
    lead = crm_service.get_crm_service(db).get_lead(lead_id, tenant_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.put("/leads/{lead_id}", response_model=schemas.Lead)
def update_lead(
    lead_id: int,
    lead: schemas.LeadUpdate,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    current_user: models.User = Depends(get_current_user)
):
    return crm_service.get_crm_service(db).update_lead(lead_id, lead, tenant_id)

@router.delete("/leads/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    current_user: models.User = Depends(get_current_user)
):
    return crm_service.get_crm_service(db).delete_lead(lead_id, tenant_id)