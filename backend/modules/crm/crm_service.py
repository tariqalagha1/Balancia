from sqlalchemy.orm import Session
from ..crm import models
from ...core import schemas
from ...core.database import get_db_context
from fastapi import Depends, HTTPException, status

from .contact_repository import ContactRepository

class CRMService:
    def __init__(self, db: Session):
        self.db = db
        self.contact_repo = ContactRepository(db)

    def create_contact(self, contact: schemas.ContactCreate, tenant_id: int):
        return self.contact_repo.create(contact.dict(), tenant_id)

    def get_contacts(self, tenant_id: int, skip: int = 0, limit: int = 100):
        return self.contact_repo.get_all(tenant_id, skip, limit)

    def get_contact(self, contact_id: int, tenant_id: int):
        contact = self.contact_repo.get_by_id(contact_id, tenant_id)
        if not contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return contact

    def update_contact(self, contact_id: int, contact: schemas.ContactUpdate, tenant_id: int):
        db_contact = self.contact_repo.update(contact_id, contact.dict(exclude_unset=True), tenant_id)
        if not db_contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return db_contact

    def delete_contact(self, contact_id: int, tenant_id: int):
        db_contact = self.contact_repo.delete(contact_id, tenant_id)
        if not db_contact:
            raise HTTPException(status_code=404, detail="Contact not found")
        return {"message": "Contact deleted"}

    def create_lead(self, lead: schemas.LeadCreate, tenant_id: int):
        db_lead = models.Lead(**lead.dict(), tenant_id=tenant_id)
        self.db.add(db_lead)
        self.db.commit()
        self.db.refresh(db_lead)
        return db_lead

    def get_leads(self, tenant_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(models.Lead)\
            .filter(models.Lead.tenant_id == tenant_id)\
            .offset(skip).limit(limit).all()

    def get_lead(self, lead_id: int, tenant_id: int):
        lead = self.db.query(models.Lead)\
            .filter(models.Lead.id == lead_id, models.Lead.tenant_id == tenant_id)\
            .first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead not found")
        return lead

    def update_lead(self, lead_id: int, lead: schemas.LeadUpdate, tenant_id: int):
        db_lead = self.get_lead(lead_id, tenant_id)
        for key, value in lead.dict(exclude_unset=True).items():
            setattr(db_lead, key, value)
        self.db.commit()
        self.db.refresh(db_lead)
        return db_lead

    def delete_lead(self, lead_id: int, tenant_id: int):
        db_lead = self.get_lead(lead_id, tenant_id)
        self.db.delete(db_lead)
        self.db.commit()
        return {"message": "Lead deleted"}

def get_crm_service(db: Session = Depends(get_db_context)):
    return CRMService(db)