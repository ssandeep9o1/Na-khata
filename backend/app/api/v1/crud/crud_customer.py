from sqlalchemy.orm import Session
from uuid import UUID

from app.api.v1 import models, schemas

def get_customer(db: Session, customer_id: UUID, shop_id: UUID) -> models.Customer | None:
    """Gets a single customer by ID, ensuring it belongs to the correct shop."""
    return db.query(models.Customer).filter(models.Customer.id == customer_id, models.Customer.shop_id == shop_id).first()

def get_customers_by_shop(db: Session, shop_id: UUID, skip: int = 0, limit: int = 100) -> list[models.Customer]:
    """Gets a list of all customers for a given shop with pagination."""
    return db.query(models.Customer).filter(models.Customer.shop_id == shop_id).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate, shop_id: UUID) -> models.Customer:
    """Creates a new customer linked to a shop."""
    db_customer = models.Customer(**customer.dict(), shop_id=shop_id)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, db_customer: models.Customer, customer_in: schemas.CustomerUpdate) -> models.Customer:
    """Updates a customer's details."""
    update_data = customer_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_customer, key, value)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, db_customer: models.Customer):
    """Deletes a customer."""
    db.delete(db_customer)
    db.commit()
    return db_customer