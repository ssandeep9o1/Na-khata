from sqlalchemy.orm import Session
from uuid import UUID

from app.api.v1 import models, schemas

def create_transaction(db: Session, transaction: schemas.TransactionCreate, shop_id: UUID) -> models.Transaction:
    """
    Creates a new transaction for a customer, linked to a shop.
    The database trigger will automatically update the customer's due_amount.
    """
    db_transaction = models.Transaction(
        **transaction.dict(),
        shop_id=shop_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transaction(db: Session, transaction_id: UUID, shop_id: UUID) -> models.Transaction | None:
    """Gets a single transaction by ID, ensuring it belongs to the correct shop."""
    return db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.shop_id == shop_id
    ).first()

def get_transactions_by_customer(
    db: Session,
    customer_id: UUID,
    shop_id: UUID,
    skip: int = 0,
    limit: int = 100
) -> list[models.Transaction]:
    """Gets a list of all transactions for a specific customer."""
    return db.query(models.Transaction).filter(
        models.Transaction.customer_id == customer_id,
        models.Transaction.shop_id == shop_id
    ).order_by(models.Transaction.created_at.desc()).offset(skip).limit(limit).all()

def delete_transaction(db: Session, db_transaction: models.Transaction):
    """
    Deletes a transaction.
    The database trigger will automatically update the customer's due_amount.
    """
    db.delete(db_transaction)
    db.commit()
    return db_transaction