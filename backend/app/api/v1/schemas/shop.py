from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from .customer import Customer
from .product import Product
from .note import Note

class ShopBase(BaseModel):
    shop_name: str
    shop_address: Optional[str] = None

class ShopCreate(ShopBase):
    pass

class ShopUpdate(ShopBase):
    shop_name: Optional[str] = None
    shop_address: Optional[str] = None

class Shop(ShopBase):
    id: UUID
    created_at: datetime
    customers: List[Customer] = []
    products: List[Product] = []
    notes: List[Note] = []

    class Config:
        orm_mode = True