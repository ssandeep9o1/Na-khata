from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.api.v1 import schemas
from app.api.v1.crud import crud_product
from app.core.database import get_db
from app.api.v1.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new product for the authenticated user's shop."""
    shop_id = UUID(current_user.get("sub"))
    return crud_product.create_product(db=db, product=product, shop_id=shop_id)

@router.get("/", response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve all products for the authenticated user's shop."""
    shop_id = UUID(current_user.get("sub"))
    products = crud_product.get_products_by_shop(db, shop_id=shop_id, skip=skip, limit=limit)
    return products

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Retrieve a specific product by ID."""
    shop_id = UUID(current_user.get("sub"))
    db_product = crud_product.get_product(db, product_id=product_id, shop_id=shop_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: UUID,
    product_in: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update a product's details."""
    shop_id = UUID(current_user.get("sub"))
    db_product = crud_product.get_product(db, product_id=product_id, shop_id=shop_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud_product.update_product(db=db, db_product=db_product, product_in=product_in)

@router.delete("/{product_id}", response_model=schemas.Product)
def delete_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a product."""
    shop_id = UUID(current_user.get("sub"))
    db_product = crud_product.get_product(db, product_id=product_id, shop_id=shop_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud_product.delete_product(db=db, db_product=db_product)