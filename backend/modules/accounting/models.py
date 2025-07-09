from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from core.database import Base
import datetime
from enum import Enum as PyEnum

class AccountType(PyEnum):
    ASSET = "Asset"
    LIABILITY = "Liability"
    EQUITY = "Equity"
    REVENUE = "Revenue"
    EXPENSE = "Expense"

class Account(Base):
    __tablename__ = "accounting_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    type = Column(Enum(AccountType), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    entries = relationship("JournalEntry", back_populates="account")

class Journal(Base):
    __tablename__ = "accounting_journals"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    entries = relationship("JournalEntry", back_populates="journal")

class JournalEntry(Base):
    __tablename__ = "accounting_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    journal_id = Column(Integer, ForeignKey("accounting_journals.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounting_accounts.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    amount = Column(Float, nullable=False)
    is_debit = Column(Boolean, nullable=False)  # True for debit, False for credit
    description = Column(Text)
    reference = Column(String(100))
    
    journal = relationship("Journal", back_populates="entries")
    account = relationship("Account", back_populates="entries")

class Tax(Base):
    __tablename__ = "accounting_taxes"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    rate = Column(Float, nullable=False)  # e.g., 0.15 for 15%
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)