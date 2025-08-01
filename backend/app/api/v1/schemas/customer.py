from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from .transaction import Transaction

class CustomerBase(BaseModel):
    name: str
    phone: str
    address: Optional[str] = None
    image_url: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    name: Optional[str] = None
    phone: Optional[str] = None

class Customer(CustomerBase):
    id: UUID
    shop_id: UUID
    due_amount: Decimal
    created_at: datetime
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True