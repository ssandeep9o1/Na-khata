from sqlalchemy.orm import Session
from uuid import UUID

from app.api.v1 import models, schemas

def get_product(db: Session, product_id: UUID, shop_id: UUID) -> models.Product | None:
    """Gets a single product by ID, ensuring it belongs to the correct shop."""
    return db.query(models.Product).filter(models.Product.id == product_id, models.Product.shop_id == shop_id).first()

def get_products_by_shop(db: Session, shop_id: UUID, skip: int = 0, limit: int = 100) -> list[models.Product]:
    """Gets a list of all products for a given shop with pagination."""
    return db.query(models.Product).filter(models.Product.shop_id == shop_id).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate, shop_id: UUID) -> models.Product:
    """Creates a new product linked to a shop."""
    db_product = models.Product(**product.dict(), shop_id=shop_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, db_product: models.Product, product_in: schemas.ProductUpdate) -> models.Product:
    """Updates a product's details."""
    update_data = product_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, db_product: models.Product):
    """Deletes a product."""
    db.delete(db_product)
    db.commit()
    return db_product