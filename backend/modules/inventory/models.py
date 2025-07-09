from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from core.database import Base
import datetime

class Warehouse(Base):
    __tablename__ = "inventory_warehouses"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    name = Column(String(100), nullable=False)
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    stocks = relationship("Stock", back_populates="warehouse")

class Product(Base):
    __tablename__ = "inventory_products"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    unit_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    stocks = relationship("Stock", back_populates="product")

class Stock(Base):
    __tablename__ = "inventory_stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("inventory_products.id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("inventory_warehouses.id"), nullable=False)
    quantity = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    
    product = relationship("Product", back_populates="stocks")
    warehouse = relationship("Warehouse", back_populates="stocks")