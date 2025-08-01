from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.v1 import schemas
from app.api.v1.crud import crud_shop
from app.core.database import get_db
from app.api.v1.dependencies.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.Shop, status_code=status.HTTP_201_CREATED)
def create_shop_for_user(
    shop: schemas.ShopCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new shop profile for the authenticated user.
    A user can only have one shop.
    """
    user_id = UUID(current_user.get("sub"))
    
    # Check if a shop already exists for this user
    db_shop = crud_shop.get_shop(db=db, user_id=user_id)
    if db_shop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Shop profile already exists for this user."
        )
        
    return crud_shop.create_shop(db=db, shop=shop, user_id=user_id)


@router.get("/me", response_model=schemas.Shop)
def read_my_shop(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve the shop profile for the currently authenticated user.
    """
    user_id = UUID(current_user.get("sub"))
    db_shop = crud_shop.get_shop(db=db, user_id=user_id)
    
    if db_shop is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shop profile not found for this user."
        )
        
    return db_shop