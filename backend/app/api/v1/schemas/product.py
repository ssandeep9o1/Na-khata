from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    name: str
    unit: str = 'piece'
    selling_price: Decimal

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    unit: Optional[str] = None
    selling_price: Optional[Decimal] = None

class Product(ProductBase):
    id: UUID
    shop_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True