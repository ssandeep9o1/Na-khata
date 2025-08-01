from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.api.v1 import schemas
from app.api.v1.crud import crud_transaction, crud_customer
from app.core.database import get_db
from app.api.v1.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Transaction, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new transaction for a customer."""
    shop_id = UUID(current_user.get("sub"))
    
    # Security Check: Ensure the customer belongs to the current user's shop
    customer = crud_customer.get_customer(db, customer_id=transaction.customer_id, shop_id=shop_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found in this shop")
        
    return crud_transaction.create_transaction(db=db, transaction=transaction, shop_id=shop_id)

@router.get("/by-customer/{customer_id}", response_model=List[schemas.Transaction])
def read_transactions_for_customer(
    customer_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve all transactions for a specific customer."""
    shop_id = UUID(current_user.get("sub"))
    # Security Check: Ensure the customer belongs to the current user's shop
    customer = crud_customer.get_customer(db, customer_id=customer_id, shop_id=shop_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found in this shop")
        
    transactions = crud_transaction.get_transactions_by_customer(
        db, customer_id=customer_id, shop_id=shop_id, skip=skip, limit=limit
    )
    return transactions

@router.get("/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve a specific transaction by ID."""
    shop_id = UUID(current_user.get("sub"))
    db_transaction = crud_transaction.get_transaction(db, transaction_id=transaction_id, shop_id=shop_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.delete("/{transaction_id}", response_model=schemas.Transaction)
def delete_transaction(
    transaction_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a transaction."""
    shop_id = UUID(current_user.get("sub"))
    db_transaction = crud_transaction.get_transaction(db, transaction_id=transaction_id, shop_id=shop_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return crud_transaction.delete_transaction(db=db, db_transaction=db_transaction)