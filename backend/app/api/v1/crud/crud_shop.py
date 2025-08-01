from sqlalchemy.orm import Session
from uuid import UUID

from app.api.v1 import models, schemas

def get_shop(db: Session, user_id: UUID) -> models.Shop | None:
    """
    Retrieves a shop profile based on the user's ID.
    A user's shop ID is the same as their auth.users ID.
    """
    return db.query(models.Shop).filter(models.Shop.id == user_id).first()

def create_shop(db: Session, shop: schemas.ShopCreate, user_id: UUID) -> models.Shop:
    """
    Creates a new shop profile for a user.
    The shop's ID is set to the user's ID to link them.
    """
    db_shop = models.Shop(**shop.dict(), id=user_id)
    db.add(db_shop)
    db.commit()
    db.refresh(db_shop)
    return db_shop