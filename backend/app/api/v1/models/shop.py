import uuid
from sqlalchemy import Column, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class Shop(Base):
    __tablename__ = "shops"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shop_name = Column(Text, nullable=False)
    shop_address = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customers = relationship("Customer", back_populates="shop", cascade="all, delete-orphan")
    products = relationship("Product", back_populates="shop", cascade="all, delete-orphan")
    transactions = relationship("Transaction", back_populates="shop", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="shop", cascade="all, delete-orphan")