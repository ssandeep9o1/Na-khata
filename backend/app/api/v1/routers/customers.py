from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.api.v1 import schemas
from app.api.v1.crud import crud_customer
from app.core.database import get_db
from app.api.v1.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new customer for the authenticated user's shop."""
    shop_id = UUID(current_user.get("sub"))
    # You might want to check for duplicate phone numbers here
    return crud_customer.create_customer(db=db, customer=customer, shop_id=shop_id)

@router.get("/", response_model=List[schemas.Customer])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve all customers for the authenticated user's shop."""
    shop_id = UUID(current_user.get("sub"))
    customers = crud_customer.get_customers_by_shop(db, shop_id=shop_id, skip=skip, limit=limit)
    return customers

@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve a specific customer by ID."""
    shop_id = UUID(current_user.get("sub"))
    db_customer = crud_customer.get_customer(db, customer_id=customer_id, shop_id=shop_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: UUID,
    customer_in: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a customer's details."""
    shop_id = UUID(current_user.get("sub"))
    db_customer = crud_customer.get_customer(db, customer_id=customer_id, shop_id=shop_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud_customer.update_customer(db=db, db_customer=db_customer, customer_in=customer_in)

@router.delete("/{customer_id}", response_model=schemas.Customer)
def delete_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a customer."""
    shop_id = UUID(current_user.get("sub"))
    db_customer = crud_customer.get_customer(db, customer_id=customer_id, shop_id=shop_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return crud_customer.delete_customer(db=db, db_customer=db_customer)