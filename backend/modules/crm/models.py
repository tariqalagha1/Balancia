from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from core.database import Base
import datetime
from enum import Enum as PyEnum

class LeadStatus(PyEnum):
    NEW = "New"
    CONTACTED = "Contacted"
    QUALIFIED = "Qualified"
    LOST = "Lost"

class Contact(Base):
    __tablename__ = "crm_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20))
    company = Column(String(100))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    leads = relationship("Lead", back_populates="contact")

class Lead(Base):
    __tablename__ = "crm_leads"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("crm_contacts.id"), nullable=False)
    source = Column(String(100))
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    contact = relationship("Contact", back_populates="leads")