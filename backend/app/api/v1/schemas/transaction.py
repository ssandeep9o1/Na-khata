from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

class TransactionBase(BaseModel):
    customer_id: UUID
    total_amount: Decimal
    amount_paid: Decimal
    transaction_type: str # 'sale' or 'payment'
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: UUID
    shop_id: UUID
    due_change: Decimal
    created_at: datetime

    class Config:
        orm_mode = True